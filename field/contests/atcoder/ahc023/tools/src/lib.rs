#![allow(non_snake_case, unused_macros)]

use std::collections::{ BTreeSet, VecDeque };
use proconio::{input, marker::*};
use rand::prelude::*;
use rand_distr::{Normal, Bernoulli, Uniform};

#[derive(Clone, Debug)]
pub struct Output {
    pub M: usize,
    pub works: Vec<Work>,
}

#[derive(Clone, Debug)]
pub struct Work {
    pub k: usize,               // 0-based
    pub i: usize,               // 0-based
    pub j: usize,               // 0-based
    pub s: usize,               // 1-based
}

#[derive(Clone, Debug)]
pub struct Input {
    pub T: usize,
    pub H: usize,
    pub W: usize,
    pub i0: usize,              // 0-based
    pub h: Vec<Vec<bool>>,
    pub v: Vec<Vec<bool>>,
    pub K: usize,
    pub S: Vec<usize>,          // 1-based
    pub D: Vec<usize>,          // 1-based
}

impl Input {
    pub fn is_valid_point(&self, x: usize, y: usize) -> bool {
        x < self.H && y < self.W
    }
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{} {} {} {}", self.T, self.H, self.W, self.i0)?;
        for h in &self.h {
            writeln!(f, "{}", h.iter().map(|&b| if b { '1' } else { '0' }).collect::<String>())?;
        }
        for v in &self.v {
            writeln!(f, "{}", v.iter().map(|&b| if b { '1' } else { '0' }).collect::<String>())?;
        }
        writeln!(f, "{}", self.K)?;
        for k in 0..self.K {
            writeln!(f, "{} {}", self.S[k], self.D[k])?;
        }
        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let mut f = proconio::source::once::OnceSource::from(f);
    input! {
        from &mut f,
        T: usize,
        H: usize,
        W: usize,
        i0: usize,
        h1: [Chars; H - 1],
        v1: [Chars; H],
        K: usize,
        SD: [(usize, usize); K],
    }
    let h = h1.iter().map(|i| i.iter().map(|&b| b == '1').collect()).collect();
    let v = v1.iter().map(|i| i.iter().map(|&b| b == '1').collect()).collect();
    let S = SD.iter().map(|x| x.0).collect();
    let D = SD.iter().map(|x| x.1).collect();
    Input { T, H, W, i0, h, v, K, S, D }
}

fn read<T: Copy + PartialOrd + std::fmt::Display + std::str::FromStr>(
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
        Err("Unexpected EOF".to_owned())
    }
}

pub fn parse_output(input: &Input, f: &str) -> Result<Output, String> {
    let mut tokens = f.split_whitespace();
    let M = read(tokens.next(), 0, input.K)?;
    let mut works = Vec::new();
    for _ in 0..M {
        let k = read(tokens.next(), 1, input.K)?;
        let i = read(tokens.next(), 0, input.H - 1)?;
        let j = read(tokens.next(), 0, input.W - 1)?;
        let s = read(tokens.next(), 1, input.T)?;
        works.push(Work{ k: k - 1, i, j, s });
    }
    if tokens.next().is_some() {
        return Err("Too many outputs".to_owned());
    }
    Ok(Output { M, works })
}

impl Output {
    pub fn validate(&self, input: &Input) -> Result<(), String> {
        // check range
        for Work { k, i: _, j: _, s, .. } in self.works.iter().cloned() {
            let ub = input.S[k];
            if s > ub {
                return Err(format!("Cannot plant crop {} after month {}", k + 1, ub));
            }
        }

        // check duplicates
        {
            let mut items = BTreeSet::new();
            for Work { k, .. } in self.works.iter() {
                if !items.insert(*k) {
                    return Err(format!("Crop {} is planted more than once", k + 1));
                }
            }
        }
        Ok(())
    }
}

pub fn compute_score(input: &Input, out: &Output) -> (i64, String) {
    if let Err(msg) = out.validate(input) {
        return (0, msg)
    }

    let mut scheduled_works: Vec<Vec<Work>> = vec![vec![]; input.T + 1];
    for w in out.works.iter().cloned() {
        scheduled_works[w.s].push(w)
    }

    let mut workspace = vec![vec![None; input.W]; input.H];
    let adj = {
        let mut adj = vec![vec![Vec::new(); input.W]; input.H];
        for i in 0..input.H {
            for j in 0..input.W {
                if i + 1 < input.H && !input.h[i][j] {
                    adj[i + 1][j].push((i, j));
                    adj[i][j].push((i + 1, j));
                }
                if j + 1 < input.W && !input.v[i][j] {
                    adj[i][j + 1].push((i, j));
                    adj[i][j].push((i, j + 1))
                }
            }
        }
        adj
    };

    let si = input.i0;
    let sj = 0;
    let start = (si, sj);
    let mut score = 0;

    for t in 1..=input.T {
        // beginning of month t
        {
            // check reachability
            if !scheduled_works[t].is_empty() {
                let mut visited = vec![vec![false; input.W]; input.H];

                if workspace[si][sj].is_none() {
                    let mut q = VecDeque::new();
                    q.push_back(start);
                    visited[si][sj] = true;

                    while !q.is_empty() {
                        let Some((x, y)) = q.pop_front() else { unreachable!() };
                        assert!(workspace[x][y].is_none());
                        for (x1, y1) in adj[x][y].iter().cloned() {
                            if input.is_valid_point(x1, y1) &&
                                workspace[x1][y1].is_none() &&
                                !visited[x1][y1] {
                                    q.push_back((x1, y1));
                                    visited[x1][y1] = true;
                                }
                        }
                    }
                }

                for &Work {k, i, j, ..} in &scheduled_works[t] {
                    if !visited[i][j] {
                        return (0, format!("{} is scheduled at unreachable position {}, {}", k + 1, i, j))
                    }
                }
            }

            // update workspace
            for &Work {k, i, j, s, ..} in &scheduled_works[t] {
                if let Some((k1, _)) = workspace[i][j] {
                    return (0, format!("Block ({}, {}) is occupied by crop {}", i, j, k1 + 1))
                } else {
                    workspace[i][j] = Some((k, s))
                }
            }
        }

        // end of month t; harvest crops
        let can_start = {
            if let Some((k, _s)) = workspace[si][sj] {
                input.D[k] == t
            } else {
                true
            }
        };

        if can_start {
            let mut q = VecDeque::new();
            q.push_back(start);
            let mut visited = vec![vec![false; input.W]; input.H];
            visited[si][sj] = true;

            while !q.is_empty() {
                let Some((i, j)) = q.pop_front() else { unreachable!() };
                if let Some((k, s)) = workspace[i][j] {
                    if input.D[k] == t {
                        workspace[i][j] = None;
                        let span = t - s + 1;
                        // this should hold because we do not
                        // allow planting crop k after month S[k]
                        assert!(span >= input.D[k] - input.S[k] + 1);
                        score += input.D[k] - input.S[k] + 1;
                    } else if input.D[k] < t {
                        return (0, format!("Cannot harvest crop {} in month {}", k + 1, input.D[k]))
                    }
                }

                for &(i1, j1) in &adj[i][j] {
                    assert!(input.is_valid_point(i1, j1));
                    let is_blocked = {
                        if let Some((k, _s)) = workspace[i1][j1] {
                            input.D[k] > t
                        } else {
                            false
                        }
                    };
                    if !is_blocked && !visited[i1][j1] {
                        q.push_back((i1, j1));
                        visited[i1][j1] = true;
                    }
                }
            }
        }
    }

    (((score as u64 * 1_000_000) as f64 / (input.H * input.W * input.T) as f64).round() as i64, String::new())
}

use rand_chacha::ChaCha20Rng;

fn gen_walls(rng: &mut ChaCha20Rng, H: usize, W: usize, distance_lb: usize) -> (Vec<Vec<bool>>, Vec<Vec<bool>>) {
    let mut h = vec![vec![false; W]; H - 1];
    let mut v = vec![vec![false; W - 1]; H];

    let adj = {
        let mut adj = vec![vec![Vec::new(); W + 1]; H + 1];
        for i in 0..=H {
            for j in 0..=W {
                if i > 0 {
                    adj[i - 1][j].push((i, j));
                    adj[i][j].push((i - 1, j));
                }
                if j > 0 {
                    adj[i][j - 1].push((i, j));
                    adj[i][j].push((i, j - 1));
                }
            }
        }
        adj
    };

    let mut marked = vec![vec![false; W + 1]; H + 1];
    for i in 0..=H {
        marked[i][0] = true;
        marked[i][W] = true;
    }
    for j in 0..=W {
        marked[0][j] = true;
        marked[H][j] = true;
    }

    loop {
        let mut candidates = Vec::new();
        let mut q = VecDeque::new();
        let mut dist = vec![vec![-1i32; W + 1]; H + 1];
        for i in 0..=H {
            for j in 0..=W {
                if marked[i][j] {
                    q.push_back((i, j));
                    dist[i][j] = 0;
                }
            }
        }

        while !q.is_empty() {
            let Some((i, j)) = q.pop_front() else { unreachable!(); };
            let dij = dist[i][j];
            for &(i1, j1) in &adj[i][j] {
                if dist[i1][j1] == -1 {
                    dist[i1][j1] = dij + 1;
                    if dij + 1 > distance_lb as i32 {
                        candidates.push((i1, j1));
                    }
                    q.push_back((i1, j1));
                }
            }
        }

        if candidates.is_empty() { break }

        let &(i, j) = candidates.iter().choose(rng).unwrap();
        let (ti, tj) = {
            let mut ti = 0;
            let mut tj = 0;
            let mut d = i + j;
            let mut num_tie = 0;
            for i1 in 0..=H {
                for j1 in 0..=W {
                    if dist[i1][j1] == 0 { // (i1, j1) is already marked
                        let d1 = i.abs_diff(i1) + j.abs_diff(j1);
                        if d > d1 { ti = i1; tj = j1; d = d1; num_tie = 1; }
                        else if d == d1 {
                            num_tie += 1;
                            if rng.gen_range(0i32, num_tie) == 0 {
                                ti = i1; tj = j1;
                            }
                        }
                    }
                }
            }
            (ti, tj)
        };
        assert!(i.abs_diff(ti) + j.abs_diff(tj) > distance_lb);

        assert!(j > 0);
        assert!(i > 0);
        assert!(ti > 0 || j == tj);
        assert!(tj > 0 || i == ti);
        if Bernoulli::new(0.5).unwrap().sample(rng) {
            if i < ti { for i1 in i..ti { v[i1][j - 1] = true; marked[i1][j] = true; } }
            else { for i1 in (ti + 1)..=i { v[i1 - 1][j - 1] = true; marked[i1][j] = true; } }
            if j < tj { for j1 in j..tj { h[ti - 1][j1] = true; marked[ti][j1] = true; } }
            else { for j1 in (tj + 1)..=j { h[ti - 1][j1 - 1] = true; marked[ti][j1] = true; } }
        } else {
            if j < tj { for j1 in j..tj { h[i - 1][j1] = true; marked[i][j1] = true; } }
            else { for j1 in (tj + 1)..=j { h[i - 1][j1 - 1] = true; marked[i][j1] = true; } }
            if i < ti { for i1 in i..ti { v[i1][tj - 1] = true; marked[i1][tj] = true; } }
            else { for i1 in (ti + 1)..=i { v[i1 - 1][tj - 1] = true; marked[i1][tj] = true; } }
        }
    }

    (h, v)
}

pub fn gen(seed: u64) -> Input {
    let mut rng = ChaCha20Rng::seed_from_u64(seed);
    let T = 100;
    let H = 20;
    let W = 20;
    let i0 = rng.gen_range(0i32, H as i32) as usize;
    let d = (seed % 4 + 1) as usize;
    let (h, v) = gen_walls(&mut rng, H, W, d);

    // let mut s = "".to_string();
    // for i in 0..=2 * H {
    //     for j in 0..=2 * W {
    //         if i % 2 == 0 && j % 2 == 0 {
    //             s.push('+')
    //         } else if i == 2 * i0 + 1 && j == 0 {
    //             s += " "
    //         } else if i == 0 || i == 2 * H {
    //             s += "--"
    //         } else if j == 0 || j == 2 * W {
    //             s += "|"
    //         } else if i % 2 == 0 {
    //             s += if h[i / 2 - 1][(j - 1) / 2] { "--" } else { "  " }
    //         } else if j % 2 == 0 {
    //             s.push(if v[(i - 1) / 2][j / 2 - 1] { '|' } else { ' ' })
    //         } else {
    //             s += "  "
    //         }
    //     }
    //     s.push('\n')
    // }
    // println!("{}", s);

    let mut sum_lk = 0;
    let normal = Normal::new(1.0, 0.25).unwrap();
    let mut D = Vec::new();
    let mut S = Vec::new();
    let limit = {
        let f = Uniform::new(1.0, 2.0).sample(&mut rng);
        ((H * W * T) as f64 * f).round() as usize
    };
    while sum_lk < limit {
        let e = normal.sample(&mut rng);
        let lk = 10f64.powf(e).round() as usize;
        if 2 <= lk && lk <= T {
            sum_lk += lk;
            let d = rng.gen_range(lk as i32, (T + 1) as i32) as usize;
            let s = d - lk + 1;
            D.push(d);
            S.push(s);
        }
    }

    Input { T, H, W, i0, h, v, K: D.len(), S, D }
}

const CHART_MARGIN: f32 = 5.0;
const BOX_SIZE: f32 = 25.0;
const LINE_COLOR: &str = "black";
const LINE_OPACITY: f32 = 1.0;
const LINE_WIDTH: f32 = 3.0;
const BOX_COLOR: &str = "black";
const BOX_WIDTH: f32 = 0.0;

use svg::Document;
use svg::node::element::Path as SvgPath;
use svg::node::element::path::Data as SvgData;
use svg::node::element::Text as SvgText;
use svg::node::Text as TextContent;

pub fn vis_default(input: &Input, out: &Output) -> String {
    let H = input.H as f32;
    let W = input.W as f32;
    let mut utils = vec![vec![0; input.W]; input.H];
    for &Work {k, i, j, ..} in &out.works {
        utils[i][j] += input.D[k] - input.S[k] + 1;
    }

    let mut svg = Document::new()
        .set("ViewBox", (0, 0, (CHART_MARGIN * 2.0 + BOX_SIZE * W) as i64, (CHART_MARGIN * 2.0 + BOX_SIZE * H) as i64))
        .set("id", "util")
        .set("width", (CHART_MARGIN * 2.0 + BOX_SIZE * W) as i64)
        .set("height", (CHART_MARGIN * 2.0 + BOX_SIZE * H) as i64);

    for i in 0..input.H {
        for j in 0..input.W {
            let cnt = utils[i][j];
            let per = cnt as f32 / input.T as f32;
            let data = 
                SvgData::new()
                .move_to((CHART_MARGIN + BOX_SIZE * j as f32, CHART_MARGIN + BOX_SIZE * i as f32))
                .line_by((0, BOX_SIZE))
                .line_by((BOX_SIZE, 0))
                .line_by((0, -BOX_SIZE))
                .line_by((-BOX_SIZE, 0))
                ;
            let p = SvgPath::new()
                .set("d", data)
                .set("stroke", BOX_COLOR)
                .set("stroke-width", BOX_WIDTH)
                .set("fill", "green")
                .set("fill-opacity", per);
            svg = svg.add(p);
            let text = SvgText::new()
                .add(TextContent::new(format!("{}", cnt)))
                .set("x", CHART_MARGIN + BOX_SIZE * (j as f32 + 0.5))
                .set("y", CHART_MARGIN + BOX_SIZE * (i as f32 + 0.5))
                .set("fill", "black")
                .set("font-size", "medium")
                .set("dominant-baseline", "central")
                .set("text-anchor", "middle");
            svg = svg.add(text)
        }
    }


    // base line
    
    for i in 0..input.H + 1 {
        for j in 0..input.W {
            if !(1 <= i && i < input.H) || input.h[i - 1][j] {
                let (color, width) = (LINE_COLOR, LINE_WIDTH);
                let data = 
                    SvgData::new()
                    .move_to((CHART_MARGIN + BOX_SIZE * j as f32, CHART_MARGIN + BOX_SIZE * i as f32))
                    .line_by((BOX_SIZE * 1.0, 0));
                let p = SvgPath::new()
                    .set("d", data)
                    .set("stroke", color)
                    .set("stroke-opacity", LINE_OPACITY)
                    .set("stroke-width", width);
                svg = svg.add(p);
            }
        }
    }

    for j in 0..input.W + 1 {
        for i in 0..input.H {
            if (!(1 <= j && j < input.W) || input.v[i][j - 1]) && !(i == input.i0 && j == 0) {
                let (color, width) = (LINE_COLOR, LINE_WIDTH);
                let data = 
                    SvgData::new()
                    .move_to((CHART_MARGIN + BOX_SIZE * j as f32, CHART_MARGIN + BOX_SIZE * i as f32))
                    .line_by((0, BOX_SIZE * 1.0));
                let p = SvgPath::new()
                    .set("d", data)
                    .set("stroke", color)
                    .set("stroke-opacity", LINE_OPACITY)
                    .set("stroke-width", width);
                svg = svg.add(p);
            }
        }
    }
    svg.to_string()
}
