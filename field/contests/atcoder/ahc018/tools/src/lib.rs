use rand::{distributions::WeightedIndex, prelude::*};

use noise::{NoiseFn, Perlin};

use itertools::Itertools;

use raqote::{Color, DrawOptions, DrawTarget, PathBuilder, Source, StrokeStyle};

use palette::{Gradient, LinSrgb};

use once_cell::sync::Lazy;

#[cfg(target_arch = "wasm32")]
use wasm_bindgen::{prelude::*, Clamped};

#[cfg(target_arch = "wasm32")]
use web_sys::{CanvasRenderingContext2d, ImageData};

#[derive(Clone, Debug)]
pub struct UnionFind {
    par: Vec<usize>,
    size: Vec<usize>,
}

impl UnionFind {
    pub fn new(n: usize) -> Self {
        UnionFind {
            par: (0..n).into_iter().collect(),
            size: vec![1; n],
        }
    }

    pub fn find(&mut self, x: usize) -> usize {
        if self.par[x] == x {
            x
        } else {
            self.par[x] = self.find(self.par[x]);
            self.par[x]
        }
    }

    pub fn unite(&mut self, x: usize, y: usize) {
        let mut x = self.find(x);
        let mut y = self.find(y);
        if self.size[x] < self.size[y] {
            ::std::mem::swap(&mut x, &mut y);
        }
        if x != y {
            self.size[x] += self.size[y];
            self.par[y] = x;
        }
    }

    pub fn same(&mut self, x: usize, y: usize) -> bool {
        self.find(x) == self.find(y)
    }
}

pub fn read<T: Copy + PartialOrd + std::fmt::Display + std::str::FromStr>(
    token: Option<&str>,
    lb: T,
    ub: T,
) -> Result<T, String> {
    if let Some(v) = token {
        if let Ok(v) = v.parse::<T>() {
            if v < lb || ub < v {
                Err(format!("Out of range: {}", v))
            } else {
                Ok(v)
            }
        } else {
            Err(format!("Parse error: {}", v))
        }
    } else {
        Err(format!("Unexpected EOF"))
    }
}

pub struct TesterInput {
    pub h: Vec<Vec<usize>>,
    pub base_cost: usize,
    pub sources: Vec<(usize, usize)>,
    pub sinks: Vec<(usize, usize)>,
}

impl std::fmt::Display for TesterInput {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let n = self.h.len();
        writeln!(
            f,
            "{} {} {} {}",
            n,
            self.sources.len(),
            self.sinks.len(),
            self.base_cost
        )?;
        for r in 0..n {
            for c in 0..n {
                write!(f, "{}", self.h[r][c])?;
                if c < n - 1 {
                    write!(f, " ")?;
                }
            }
            writeln!(f)?;
        }
        for (r, c) in self.sources.iter() {
            writeln!(f, "{} {}", r, c)?;
        }
        for (r, c) in self.sinks.iter() {
            writeln!(f, "{} {}", r, c)?;
        }
        Ok(())
    }
}

impl std::str::FromStr for TesterInput {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut tokens = s.split_whitespace();
        let n = read(tokens.next(), N, N)?;
        let w = read(tokens.next(), MIN_W, MAX_W)?;
        let k = read(tokens.next(), MIN_K, MAX_K)?;
        let base_cost = read(tokens.next(), 0, usize::MAX)?;

        let mut h = vec![vec![0; n]; n];
        for r in 0..n {
            for c in 0..n {
                h[r][c] = read(tokens.next(), MIN_H, MAX_H)?;
            }
        }

        let mut sources = vec![];
        let mut sinks = vec![];
        for _ in 0..w {
            sources.push((
                read(tokens.next(), 0, n - 1)?,
                read(tokens.next(), 0, n - 1)?,
            ));
        }
        for _ in 0..k {
            sinks.push((
                read(tokens.next(), 0, n - 1)?,
                read(tokens.next(), 0, n - 1)?,
            ))
        }

        Ok(TesterInput {
            h,
            base_cost,
            sources,
            sinks,
        })
    }
}

pub struct DigOp {
    r: usize,
    c: usize,
    p: usize,
}

impl std::str::FromStr for DigOp {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut tokens = s.split_whitespace();
        let r = read(tokens.next(), 0, N - 1)?;
        let c = read(tokens.next(), 0, N - 1)?;
        let p = read(tokens.next(), 1, MAX_H)?;
        Ok(DigOp { r, c, p })
    }
}

pub struct DigOpWithComment {
    comments: Vec<String>,
    op: DigOp,
}

type ContestantOutput = Vec<DigOpWithComment>;

pub struct VisualizeData {
    pub input: TesterInput,
    pub output: ContestantOutput,
}

pub fn parse_visualize_data(input: &str, output: &str) -> Result<VisualizeData, String> {
    let input = input.parse::<TesterInput>()?;
    let output = {
        let mut commands = vec![];
        let mut comments = vec![];
        for line in output.trim().lines() {
            if let Some(comment) = line.strip_prefix("#") {
                comments.push(comment.to_owned());
            } else {
                commands.push(DigOpWithComment {
                    comments: comments.clone(),
                    op: line.parse::<DigOp>()?,
                });
                comments.clear();
            }
        }
        commands
    };
    Ok(VisualizeData { input, output })
}

const N: usize = 200;
const MIN_W: usize = 1;
const MAX_W: usize = 4;
const MIN_K: usize = 1;
const MAX_K: usize = 10;
const C_CHOICES: [usize; 8] = [1, 2, 4, 8, 16, 32, 64, 128];
const MIN_H: usize = 10;
const MAX_H: usize = 5000;

pub fn gen(
    seed: u64,
    w: Option<usize>,
    k: Option<usize>,
    c: Option<usize>,
) -> Result<TesterInput, String> {
    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);

    let w: usize = w.unwrap_or(rng.gen_range(MIN_W as u64..=MAX_W as u64) as usize);
    let k: usize = k.unwrap_or(rng.gen_range(MIN_K as u64..=MAX_K as u64) as usize);
    let c: usize = c.unwrap_or(*C_CHOICES.choose(&mut rng).unwrap());

    if !(MIN_W..=MAX_W).contains(&w) {
        return Err(format!("w must be in range [{MIN_W}, {MAX_W}]"));
    }
    if !(MIN_K..=MAX_K).contains(&k) {
        return Err(format!("k must be in range [{MIN_K}, {MAX_K}]"));
    }
    if !C_CHOICES.contains(&c) {
        return Err(format!("c must be one of {C_CHOICES:?}"));
    }

    let mut h: Vec<Vec<f64>> = vec![vec![0.0; N]; N];

    // Perlin noise
    for (freq, amp) in [
        (rng.gen_range(2.0..8.0), 1.0),
        (rng.gen_range(10.0..20.0), 0.2),
    ] {
        let perlin = Perlin::new(rng.gen());

        let y_offset = rng.gen::<f64>();
        let x_offset = rng.gen::<f64>();

        for r in 0..N {
            for c in 0..N {
                let y = y_offset + (r as f64 / N as f64) * freq;
                let x = x_offset + (c as f64 / N as f64) * freq;
                h[r][c] += perlin.get([y, x]) * amp;
            }
        }
    }

    // apply logistic function
    for r in 0..N {
        for c in 0..N {
            h[r][c] = 1.0 / (1.0 + (-3.0 * (h[r][c] - 0.25)).exp());
        }
    }

    // apply power function
    let power = rng.gen_range(2.0..4.0);
    for r in 0..N {
        for c in 0..N {
            h[r][c] = h[r][c].powf(power);
        }
    }

    // linearly rescale h to a range [MIN_H, MAX_H]
    let mut min_h = f64::MAX;
    let mut max_h = f64::MIN;
    for r in 0..N {
        for c in 0..N {
            min_h = min_h.min(h[r][c]);
            max_h = max_h.max(h[r][c]);
        }
    }
    for r in 0..N {
        for c in 0..N {
            h[r][c] = (MIN_H as f64 + (h[r][c] - min_h) / (max_h - min_h) * (MAX_H - MIN_H) as f64)
                .round();
        }
    }

    // For each 0 <= r, c < N, dist takes the value r * N + c with probability proportional to 1 / h[r][c]
    let weights: Vec<f64> = h.concat().iter().map(|x| 1.0 / x).collect();
    let dist = WeightedIndex::new(&weights).unwrap();

    // generate sources and sinks
    let (sources, sinks) = 'outer: loop {
        let mut sources = vec![];
        let mut sinks = vec![];

        for _ in 0..w {
            let i = dist.sample(&mut rng);
            sources.push((i / N, i % N));
        }
        for _ in 0..k {
            let i = dist.sample(&mut rng);
            sinks.push((i / N, i % N));
        }

        let points = [sources.clone(), sinks.clone()].concat();

        // the Manhattan distance between every pair must be greater than or equal to round(400 / (w + k))
        for (&(a, b), &(c, d)) in points.iter().tuple_combinations() {
            if a.abs_diff(c) + b.abs_diff(d) < (400.0 / (w + k) as f64).round() as usize {
                continue 'outer;
            }
        }

        break (sources, sinks);
    };

    Ok(TesterInput {
        h: h.iter()
            .map(|row| row.iter().map(|&v| v as usize).collect())
            .collect(),
        base_cost: c,
        sources,
        sinks,
    })
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn generate(
    seed: u64,
    w: Option<usize>,
    k: Option<usize>,
    c: Option<usize>,
) -> Result<String, JsError> {
    let w = w.filter(|&w| w != 0);
    let k = k.filter(|&k| k != 0);
    let c = c.filter(|&c| c != 0);
    gen(seed, w, k, c)
        .map(|t| t.to_string())
        .map_err(|e| JsError::new(&e))
}

pub struct Outcome {
    pub h: Vec<Vec<usize>>,
    pub water: Vec<Vec<bool>>,
    pub total_cost: u64,
}

#[derive(Clone, Copy, PartialEq)]
pub enum DigResult {
    NotDestructed = 0,
    Destructed = 1,
    ConditionsSatisfied = 2,
}

pub struct Sim {
    init_h: Vec<Vec<usize>>,
    h: Vec<Vec<usize>>,
    base_cost: usize,
    sources: Vec<(usize, usize)>,
    sinks: Vec<(usize, usize)>,
    total_cost: u64,
    uf: UnionFind,
}

impl Sim {
    pub fn new(input: &TesterInput) -> Self {
        Sim {
            init_h: input.h.clone(),
            h: input.h.clone(),
            base_cost: input.base_cost,
            sources: input.sources.clone(),
            sinks: input.sinks.clone(),
            total_cost: 0,
            uf: UnionFind::new(N * N),
        }
    }

    pub fn cur_cost(&self) -> u64 {
        self.total_cost
    }

    pub fn dig(&mut self, op: &DigOp) -> Result<DigResult, String> {
        if !(0..N).contains(&op.r) || !(0..N).contains(&op.c) || !(1..=MAX_H).contains(&op.p) {
            return Err(format!("invalid operation: ({}, {}; {})", op.r, op.c, op.p));
        }
        if self.h[op.r][op.c] == 0 {
            return Err(format!(
                "invalid operation: ({}, {}) has already been destructed",
                op.r, op.c
            ));
        }

        self.h[op.r][op.c] = 0.max(self.h[op.r][op.c] as isize - op.p as isize) as usize;
        self.total_cost += self.base_cost as u64 + op.p as u64;

        if self.h[op.r][op.c] == 0 {
            for (dr, dc) in [(0, -1), (-1, 0), (0, 1), (1, 0)] {
                let nr = op.r as isize + dr;
                let nc = op.c as isize + dc;
                if (0..N as isize).contains(&nr) && (0..N as isize).contains(&nc) {
                    let nr = nr as usize;
                    let nc = nc as usize;
                    if self.h[nr][nc] == 0 {
                        self.uf.unite(op.r * N + op.c, nr * N + nc);
                    }
                }
            }
        }

        let satisfied = self.sinks.iter().all(|(a, b)| {
            self.sources
                .iter()
                .any(|(c, d)| self.uf.same(a * N + b, c * N + d))
        });

        if satisfied {
            Ok(DigResult::ConditionsSatisfied)
        } else if self.h[op.r][op.c] == 0 {
            Ok(DigResult::Destructed)
        } else {
            Ok(DigResult::NotDestructed)
        }
    }

    pub fn compute_score(&mut self) -> (Outcome, Option<String>) {
        let mut water = vec![vec![false; N]; N];

        for r in 0..N {
            for c in 0..N {
                let connected_to_sources = self
                    .sources
                    .iter()
                    .any(|(a, b)| self.uf.same(r * N + c, a * N + b));

                water[r][c] = connected_to_sources && (self.h[r][c] == 0);
            }
        }

        let dry_sink = self.sinks.iter().position(|&(a, b)| !water[a][b]);

        let outcome = Outcome {
            h: self.h.clone(),
            water,
            total_cost: self.total_cost,
        };

        let error = dry_sink.map(|i| format!("House {i} is unreachable from water sources"));

        (outcome, error)
    }
}

static H_PALETTE: Lazy<Vec<Color>> = Lazy::new(|| {
    let colors: Vec<LinSrgb> = Gradient::from([
        (
            0.0,
            LinSrgb::new(242.0 / 255.0, 196.0 / 255.0, 179.0 / 255.0),
        ),
        (
            0.1,
            LinSrgb::new(217.0 / 255.0, 129.0 / 255.0, 98.0 / 255.0),
        ),
        (0.3, LinSrgb::new(166.0 / 255.0, 87.0 / 255.0, 41.0 / 255.0)),
        (0.6, LinSrgb::new(89.0 / 255.0, 34.0 / 255.0, 2.0 / 255.0)),
        (1.0, LinSrgb::new(64.0 / 255.0, 24.0 / 255.0, 1.0 / 255.0)),
    ])
    .take(MAX_H + 1)
    .collect();
    colors
        .into_iter()
        .map(|c| {
            Color::new(
                255u8,
                (255.0 * c.red) as u8,
                (255.0 * c.green) as u8,
                (255.0 * c.blue) as u8,
            )
        })
        .collect()
});
const COL_DESTRUCTED: Lazy<Color> = Lazy::new(|| Color::new(255u8, 140u8, 140u8, 140u8));
const COL_WATER: Lazy<Color> = Lazy::new(|| Color::new(255u8, 115u8, 204u8, 218u8));
const COL_SOURCE: Lazy<Color> = Lazy::new(|| Color::new(255u8, 0u8, 6u8, 177u8));
const COL_SINK_WATERED: Lazy<Color> = Lazy::new(|| Color::new(255u8, 67u8, 191u8, 103u8));
const COL_SINK_NOT_WATERED: Lazy<Color> = Lazy::new(|| Color::new(255u8, 64u8, 64u8, 64u8));
const COL_LAST_DIG: Lazy<Color> = Lazy::new(|| Color::new(255u8, 255u8, 0u8, 255u8));
const COL_WHITE: Lazy<Color> = Lazy::new(|| Color::new(255u8, 255u8, 255u8, 255u8));

fn cell_color(h: usize, water: bool) -> Color {
    if h == 0 {
        if water {
            *COL_WATER
        } else {
            *COL_DESTRUCTED
        }
    } else {
        H_PALETTE[h]
    }
}

#[derive(Clone)]
#[cfg_attr(target_arch = "wasm32", wasm_bindgen)]
pub struct DigInfo {
    pub x: usize,
    pub y: usize,
    pub power: usize,
    pub prev_stur: usize,
    pub curr_stur: usize,
    pub init_stur: usize,
}

#[cfg_attr(target_arch = "wasm32", wasm_bindgen(getter_with_clone))]
pub struct VisResult {
    pub cost: u64,
    pub last_dig: Option<DigInfo>,
    pub comment: Option<String>,
}

pub fn vis(data: &VisualizeData, turn: usize) -> (VisResult, DrawTarget) {
    let mut sim = Sim::new(&data.input);

    let mut last_dig = None;
    for (i, dig_op) in data.output[..turn].iter().enumerate() {
        let prev = sim.h[dig_op.op.r][dig_op.op.c];
        sim.dig(&dig_op.op).unwrap();
        if i == turn - 1 {
            last_dig = Some(DigInfo {
                x: dig_op.op.c,
                y: dig_op.op.r,
                power: dig_op.op.p,
                prev_stur: prev,
                curr_stur: sim.h[dig_op.op.r][dig_op.op.c],
                init_stur: sim.init_h[dig_op.op.r][dig_op.op.c],
            });
        }
    }

    let (outcome, _) = sim.compute_score();

    const SC: usize = 4;
    fn cell_coord(r: usize, c: usize) -> (f32, f32) {
        ((r * SC) as f32, (c * SC) as f32)
    }

    let mut img = DrawTarget::new((N * SC) as i32, (N * SC) as i32);

    for r in 0..N {
        for c in 0..N {
            let color = cell_color(outcome.h[r][c], outcome.water[r][c]);
            let color = (color.a() as u32) << 24
                | (color.r() as u32) << 16
                | (color.g() as u32) << 8
                | (color.b() as u32);

            let data = img.get_data_mut();
            for dr in 0..SC {
                for dc in 0..SC {
                    let rr = r * SC + dr;
                    let cc = c * SC + dc;
                    data[rr * 800 + cc] = color;
                }
            }
        }
    }

    fn stroke_rect(
        img: &mut DrawTarget,
        x: f32,
        y: f32,
        width: f32,
        height: f32,
        color: Color,
        stroke_width: f32,
    ) {
        let path = {
            let mut pb = PathBuilder::new();
            pb.move_to(x, y);
            pb.line_to(x + width, y);
            pb.line_to(x + width, y + height);
            pb.line_to(x, y + height);
            pb.line_to(x, y);
            pb.line_to(x + width, y);
            pb.finish()
        };
        let mut style = StrokeStyle::default();
        style.width = stroke_width + 2.0;
        img.stroke(
            &path,
            &Source::from(*COL_WHITE),
            &style,
            &DrawOptions::new(),
        );
        style.width = stroke_width;
        img.stroke(&path, &Source::from(color), &style, &DrawOptions::new())
    }

    fn stroke_triangle(
        img: &mut DrawTarget,
        x: f32,
        y: f32,
        width: f32,
        height: f32,
        color: Color,
        stroke_width: f32,
    ) {
        let y = y - SC as f32 * 3.0 / 4.0;
        let path = {
            let mut pb = PathBuilder::new();
            pb.move_to(x + width / 2.0, y);
            pb.line_to(x + width, y + height);
            pb.line_to(x, y + height);
            pb.line_to(x + width / 2.0, y);
            pb.line_to(x + width, y + height);
            pb.finish()
        };
        let mut style = StrokeStyle::default();
        style.width = stroke_width + 2.0;
        img.stroke(
            &path,
            &Source::from(*COL_WHITE),
            &style,
            &DrawOptions::new(),
        );
        style.width = stroke_width;
        img.stroke(&path, &Source::from(color), &style, &DrawOptions::new())
    }

    const MARKER_SIZE: f32 = 16.0;
    for &(r, c) in &data.input.sources {
        let (y, x) = cell_coord(r, c);
        stroke_rect(
            &mut img,
            x + SC as f32 / 2.0 - MARKER_SIZE / 2.0,
            y + SC as f32 / 2.0 - MARKER_SIZE / 2.0,
            MARKER_SIZE,
            MARKER_SIZE,
            *COL_SOURCE,
            SC as f32 * 3.0 / 4.0,
        );
    }

    for &(r, c) in &data.input.sinks {
        let color = if outcome.water[r][c] {
            *COL_SINK_WATERED
        } else {
            *COL_SINK_NOT_WATERED
        };
        let (y, x) = cell_coord(r, c);

        stroke_triangle(
            &mut img,
            x + SC as f32 / 2.0 - MARKER_SIZE / 2.0,
            y + SC as f32 / 2.0 - MARKER_SIZE / 2.0,
            MARKER_SIZE,
            MARKER_SIZE,
            color,
            SC as f32 * 3.0 / 4.0,
        );
    }

    let mut comments = vec![];
    if let Some(&DigOpWithComment {
        comments: ref cs,
        op: DigOp { r, c, p: _ },
    }) = data.output.get(turn - 1)
    {
        comments = cs.clone();
        let (y, x) = cell_coord(r, c);
        stroke_rect(
            &mut img,
            x - SC as f32 / 2.0,
            y - SC as f32 / 2.0,
            SC as f32 * 2.0,
            SC as f32 * 2.0,
            *COL_LAST_DIG,
            SC as f32 / 2.0,
        );
    }
    (
        VisResult {
            cost: outcome.total_cost,
            last_dig,
            comment: if comments.is_empty() {
                None
            } else {
                Some(comments.join("\n"))
            },
        },
        img,
    )
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn visualize(
    ctx: &CanvasRenderingContext2d,
    input: &str,
    output: &str,
    turn: usize,
) -> Result<VisResult, JsError> {
    let data = parse_visualize_data(input, output).map_err(|e| JsError::new(&e))?;
    let (vis_res, img) = vis(&data, turn);

    let width = img.width() as usize;
    let height = img.height() as usize;
    let img_data = img.into_inner();
    let mut img_data_u8 = vec![0u8; width * height * 4];
    for (i, col) in img_data.into_iter().enumerate() {
        let (a, r, g, b) = (
            (col >> 24) as u8,
            (col >> 16 & 255) as u8,
            (col >> 8 & 255) as u8,
            (col & 255) as u8,
        );
        img_data_u8[4 * i + 0] = r;
        img_data_u8[4 * i + 1] = g;
        img_data_u8[4 * i + 2] = b;
        img_data_u8[4 * i + 3] = a;
    }

    ctx.put_image_data(
        &ImageData::new_with_u8_clamped_array_and_sh(
            Clamped(&mut img_data_u8),
            width as u32,
            height as u32,
        )
        .map_err(|_| JsError::new("failed to create ImageData"))?,
        0.0,
        0.0,
    )
    .map_err(|_| JsError::new("failed to put ImageData"))?;

    Ok(vis_res)
}

#[cfg_attr(target_arch = "wasm32", wasm_bindgen(getter_with_clone))]
pub struct SolInfo {
    pub error: Option<String>,
    pub total_cost: u64,
    pub max_turn: usize,
}

pub fn validate_sol(data: &VisualizeData) -> SolInfo {
    let mut sim = Sim::new(&data.input);
    let mut invalid_op = None;
    for t in 0..data.output.len() {
        let op = &data.output[t];
        match sim.dig(&op.op) {
            Ok(_) => {}
            Err(err) => {
                invalid_op = Some((t, err));
                break;
            }
        }
    }

    if let Some((first_fail_turn, err)) = invalid_op {
        SolInfo {
            error: Some(err),
            total_cost: sim.cur_cost(),
            max_turn: first_fail_turn,
        }
    } else {
        let (outcome, error) = sim.compute_score();
        SolInfo {
            error,
            total_cost: outcome.total_cost,
            max_turn: data.output.len(),
        }
    }
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn get_sol_info(input: &str, output: &str) -> Result<SolInfo, JsError> {
    let data = parse_visualize_data(input, output).map_err(|e| JsError::new(&e))?;
    Ok(validate_sol(&data))
}
