#![allow(non_snake_case, unused_macros)]

use itertools::Itertools;
use proconio::input;
use rand::prelude::*;
use std::ops::RangeBounds;
use svg::node::element::{Group, Line, Rectangle, Style, Symbol, Text, Title, Use};

pub trait SetMinMax {
    fn setmin(&mut self, v: Self) -> bool;
    fn setmax(&mut self, v: Self) -> bool;
}
impl<T> SetMinMax for T
where
    T: PartialOrd,
{
    fn setmin(&mut self, v: T) -> bool {
        *self > v && {
            *self = v;
            true
        }
    }
    fn setmax(&mut self, v: T) -> bool {
        *self < v && {
            *self = v;
            true
        }
    }
}

#[macro_export]
macro_rules! mat {
	($($e:expr),*) => { Vec::from(vec![$($e),*]) };
	($($e:expr,)*) => { Vec::from(vec![$($e),*]) };
	($e:expr; $d:expr) => { Vec::from(vec![$e; $d]) };
	($e:expr; $d:expr $(; $ds:expr)+) => { Vec::from(vec![mat![$e $(; $ds)*]; $d]) };
}

#[derive(Clone, Debug)]
pub struct Input {
    n: usize,
    A: Vec<Vec<i32>>,
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{}", self.n)?;
        for i in 0..self.n {
            writeln!(f, "{}", self.A[i].iter().join(" "))?;
        }
        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let f = proconio::source::once::OnceSource::from(f);
    input! {
        from f,
        n: usize,
        A: [[i32; n]; n],
    }
    Input { n, A }
}

pub fn read<T: Copy + PartialOrd + std::fmt::Display + std::str::FromStr, R: RangeBounds<T>>(
    token: Option<&str>,
    range: R,
) -> Result<T, String> {
    if let Some(v) = token {
        if let Ok(v) = v.parse::<T>() {
            if !range.contains(&v) {
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

pub struct Output {
    pub out: Vec<Vec<char>>,
}

pub fn parse_output(input: &Input, f: &str) -> Result<Output, String> {
    let out = f.trim().lines().map(|s| s.trim().chars().collect_vec()).collect_vec();
    if out.len() != input.A.len() {
        return Err("Invalid output format".to_owned());
    }
    if out.iter().any(|s| s.len() == 0 || s.len() > 10000) {
        return Err("Illegal output length".to_owned());
    }
    Ok(Output { out })
}

pub fn gen(seed: u64) -> Input {
    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
    let n = 5;
    let mut order = (0..n * n).collect_vec();
    order.shuffle(&mut rng);
    let mut A = mat![0; n; n];
    for i in 0..n {
        for j in 0..n {
            A[i][j] = order[i * n + j] as i32;
        }
    }
    Input { n, A }
}

pub fn compute_score(input: &Input, out: &Output) -> (i64, String) {
    let (mut score, err, _) = compute_score_details(input, out, out.out.iter().map(|s| s.len()).max().unwrap());
    if err.len() > 0 {
        score = 0;
    }
    (score, err)
}

const DIJ: [(usize, usize); 4] = [(!0, 0), (1, 0), (0, !0), (0, 1)];
const DIR: [char; 4] = ['U', 'D', 'L', 'R'];

pub struct State {
    n: usize,
    board: Vec<Vec<i32>>,
    A: Vec<Vec<i32>>,
    B: Vec<Vec<i32>>,
    pos: Vec<(usize, usize, i32)>,
    done: i32,
    turn: i64,
}

impl State {
    fn new(input: &Input) -> Self {
        let mut board = mat![-1; input.n; input.n];
        let mut A = input.A.iter().map(|a| a.iter().copied().rev().collect_vec()).collect_vec();
        for i in 0..input.n {
            board[i][0] = A[i].pop().unwrap();
        }
        State {
            n: input.n,
            board,
            A,
            B: vec![vec![]; input.n],
            pos: (0..input.n).map(|i| (i, 0, -1)).collect_vec(),
            done: 0,
            turn: 0,
        }
    }
    fn apply(&mut self, mv: &[char]) -> Result<(), String> {
        self.turn += 1;
        let mut to = vec![(!0, !0, -1); self.n];
        for i in 0..self.n {
            let (mut x, mut y, mut z) = self.pos[i];
            match mv[i] {
                '.' => (),
                'P' => {
                    if x == !0 {
                        return Err(format!("Crane {i} has already bombed."));
                    } else if z != -1 {
                        return Err(format!("Crane {i} holds a container."));
                    } else if self.board[x][y] == -1 {
                        return Err(format!("No container at ({x}, {y})."));
                    } else {
                        z = self.board[x][y];
                        self.board[x][y] = -1;
                    }
                }
                'Q' => {
                    if x == !0 {
                        return Err(format!("Crane {i} has already bombed."));
                    } else if z == -1 {
                        return Err(format!("Crane {i} does not hold a container."));
                    } else if self.board[x][y] != -1 {
                        return Err(format!("Container already exists at ({x}, {y})."));
                    } else {
                        self.board[x][y] = z;
                        z = -1;
                    }
                }
                'U' | 'D' | 'L' | 'R' => {
                    if x == !0 {
                        return Err(format!("Crane {i} has already bombed."));
                    }
                    let dir = (0..4).find(|&d| DIR[d] == mv[i]).unwrap();
                    let (dx, dy) = DIJ[dir];
                    x += dx;
                    y += dy;
                    if x >= self.n || y >= self.n {
                        return Err(format!("Crane {i} moved out of the board."));
                    } else if i > 0 && z != -1 && self.board[x][y] != -1 {
                        return Err(format!("Cranes {i} cannot move to a square that contains a container."));
                    }
                }
                'B' => {
                    if x == !0 {
                        return Err(format!("Crane {i} has already bombed."));
                    }
                    if z != -1 {
                        return Err(format!("Crane {i} holds a container."));
                    }
                    x = !0;
                    y = !0;
                }
                c => {
                    return Err(format!("Invalid move: {}", c));
                }
            }
            to[i] = (x, y, z);
        }
        for i in 0..self.n {
            if to[i].0 == !0 {
                continue;
            }
            for j in 0..i {
                if to[j].0 == !0 {
                    continue;
                }
                if (to[i].0, to[i].1) == (to[j].0, to[j].1) {
                    return Err(format!("Crane {j} and {i} collided."));
                } else if (to[i].0, to[i].1) == (self.pos[j].0, self.pos[j].1)
                    && (to[j].0, to[j].1) == (self.pos[i].0, self.pos[i].1)
                {
                    return Err(format!("Crane {i} and {j} collided."));
                }
            }
        }
        self.pos = to;
        for i in 0..self.n {
            if self.board[i][0] == -1 && self.A[i].len() > 0 && self.pos.iter().all(|p| p.2 == -1 || (p.0, p.1) != (i, 0)) {
                self.board[i][0] = self.A[i].pop().unwrap();
            }
            if self.board[i][self.n - 1] != -1 {
                self.done += 1;
                if (self.n * i) as i32 <= self.board[i][self.n - 1] && self.board[i][self.n - 1] < (self.n * (i + 1)) as i32 {
                    self.B[i].push(self.board[i][self.n - 1]);
                }
                self.board[i][self.n - 1] = -1;
            }
        }
        Ok(())
    }
    fn score(&self) -> i64 {
        let A = self.turn;
        let mut B = 0;
        let mut C = self.done as i64;
        let D = (self.n * self.n) as i64 - self.done as i64;
        for i in 0..self.n {
            C -= self.B[i].len() as i64;
            for a in 0..self.B[i].len() {
                for b in a + 1..self.B[i].len() {
                    if self.B[i][a] > self.B[i][b] {
                        B += 1;
                    }
                }
            }
        }
        let score = A + B * 100 + C * 10000 + D * 1000000;
        score
    }
}

pub fn compute_score_details(input: &Input, out: &Output, t: usize) -> (i64, String, State) {
    let mut state = State::new(input);
    for k in 0..t {
        let mv = (0..input.n).map(|i| out.out[i].get(k).copied().unwrap_or('.')).collect_vec();
        if let Err(err) = state.apply(&mv) {
            return (0, format!("{err} (turn {k})"), state);
        }
    }
    let score = state.score();
    (score, String::new(), state)
}

/// 0 <= val <= 1
pub fn color(mut val: f64) -> String {
    val.setmin(1.0);
    val.setmax(0.0);
    let (r, g, b) = if val < 0.5 {
        let x = val * 2.0;
        (
            30. * (1.0 - x) + 144. * x,
            144. * (1.0 - x) + 255. * x,
            255. * (1.0 - x) + 30. * x,
        )
    } else {
        let x = val * 2.0 - 1.0;
        (
            144. * (1.0 - x) + 255. * x,
            255. * (1.0 - x) + 30. * x,
            30. * (1.0 - x) + 70. * x,
        )
    };
    format!("#{:02x}{:02x}{:02x}", r.round() as i32, g.round() as i32, b.round() as i32)
}

pub fn rect(x: usize, y: usize, w: usize, h: usize, fill: &str) -> Rectangle {
    Rectangle::new()
        .set("x", x)
        .set("y", y)
        .set("width", w)
        .set("height", h)
        .set("fill", fill)
}

pub fn group(title: String) -> Group {
    Group::new().add(Title::new(title))
}

pub fn vis_default(input: &Input, out: &Output) -> (i64, String, String) {
    let (mut score, err, svg) = vis(input, &out, out.out.iter().map(|s| s.len()).max().unwrap());
    if err.len() > 0 {
        score = 0;
    }
    (score, err, svg)
}

// https://www.svgrepo.com/svg/175680/crane
pub const CRANE: &'static str = r#"<path d="m396.1,11h-238.9c-7.5-0.5-22.1,6.8-20.5,22.3l19.9,211.2c1,10.5 9.9,18.5 20.5,18.5h79v46.9c0,11.3 9.2,20.4 20.5,20.4 36,0 65.3,29.1 65.3,64.9s-29.3,64.9-65.3,64.9c-36,0-65.3-29.1-65.3-64.9 0-11.3-9.2-20.4-20.5-20.4-11.3,0-20.5,9.1-20.5,20.4 0,58.3 47.7,105.7 106.4,105.7 58.7,0 106.4-47.4 106.4-105.7 0-51.3-37-94.2-85.9-103.8v-28.4h79c10.6,0 19.5-8 20.5-18.5l19.9-211.2c0.8-6.8-3.2-21.6-20.5-22.3zm-38.6,211.2h-161.7l-16-170.4h193.8l-16.1,170.4z"/>"#;

pub fn vis(input: &Input, out: &Output, t: usize) -> (i64, String, String) {
    let S = 40;
    let D = 600 / (input.n + 2);
    let W = D * (input.n + 2) + D / input.n;
    let H = D * input.n + S;
    let (score, err, state) = compute_score_details(input, out, t);
    let mut doc = svg::Document::new()
        .set("id", "vis")
        .set("viewBox", (-5, -5, W + 10, H + 10))
        .set("width", W + 10)
        .set("height", H + 10)
        .set("style", "background-color:white");
    doc = doc.add(Style::new(format!(
        "text {{text-anchor: middle;dominant-baseline: central;}}"
    )));
    doc = doc.add(
        Symbol::new()
            .set("id", "crane")
            .set("viewBox", (0, 0, 512, 512))
            .add(svg::node::Blob::new(CRANE)),
    );
    for i in 0..state.n {
        let mv = out.out[i].get(t).copied().unwrap_or('.');
        doc = doc.add(
            Text::new(format!("{i}: {mv}"))
                .set("x", D * (1 + i) + D / 2)
                .set("y", S / 2)
                .set("font-size", S / 2)
                .set("fill", "black"),
        );
    }
    for i in 0..=state.n {
        doc = doc.add(
            Line::new()
                .set("x1", D)
                .set("y1", S + D * i)
                .set("x2", D * (1 + state.n))
                .set("y2", S + D * i)
                .set("stroke", "gray")
                .set("stroke-width", 1),
        );
        doc = doc.add(
            Line::new()
                .set("x1", D * (1 + i))
                .set("y1", S)
                .set("x2", D * (1 + i))
                .set("y2", S + D * state.n)
                .set("stroke", "gray")
                .set("stroke-width", 1),
        );
    }
    for i in 0..state.n {
        for j in 0..state.A[i].len() {
            doc = doc.add(rect(
                D / input.n * j,
                S + D * i,
                D / input.n,
                D,
                &color(state.A[i][j] as f64 / (input.n * input.n - 1) as f64),
            ));
            doc = doc.add(
                Text::new(format!("{}", state.A[i][j]))
                    .set("x", D / input.n * j + D / input.n / 2)
                    .set("y", S + D * i + D / 2)
                    .set("font-size", D / input.n / 2)
                    .set("fill", "black"),
            );
        }
        for j in 0..state.B[i].len() {
            doc = doc.add(rect(
                D * (1 + state.n) + D / input.n * (input.n - j),
                S + D * i,
                D / input.n,
                D,
                &color(state.B[i][j] as f64 / (input.n * input.n - 1) as f64),
            ));
            doc = doc.add(
                Text::new(format!("{}", state.B[i][j]))
                    .set("x", D * (1 + state.n) + D / input.n * (input.n - j) + D / input.n / 2)
                    .set("y", S + D * i + D / 2)
                    .set("font-size", D / input.n / 2)
                    .set("fill", "black"),
            );
        }
    }
    for i in 0..state.n {
        for j in 0..state.n {
            if state.board[i][j] != -1 {
                doc = doc.add(rect(
                    D * (1 + j),
                    S + D * i + D / 2,
                    D,
                    D / 2,
                    &color(state.board[i][j] as f64 / (input.n * input.n - 1) as f64),
                ));
                doc = doc.add(
                    Text::new(format!("{}", state.board[i][j]))
                        .set("x", D * (1 + j) + D / 2)
                        .set("y", S + D * i + D / 2 + D / 4)
                        .set("font-size", D / 4)
                        .set("fill", "black"),
                );
            }
        }
    }
    for i in 0..state.n {
        if state.pos[i].0 != !0 {
            doc = doc.add(
                Use::new()
                    .set("x", D * (1 + state.pos[i].1) + D / 4)
                    .set("y", S + D * state.pos[i].0)
                    .set("width", D / 2)
                    .set("height", D / 2)
                    .set("href", "#crane"),
            );
            doc = doc.add(
                Text::new(format!("{}", i))
                    .set("x", D * (1 + state.pos[i].1) + D / 2 + 2)
                    .set("y", S + D * state.pos[i].0 + D / 8)
                    .set("font-size", D / 6)
                    .set("fill", "black"),
            );
            if state.pos[i].2 != -1 {
                if i == 0 {
                    doc = doc.add(rect(
                        D * (1 + state.pos[i].1),
                        S + D * state.pos[i].0,
                        D,
                        D / 2,
                        &color(state.pos[i].2 as f64 / (input.n * input.n - 1) as f64),
                    ));
                    doc = doc.add(
                        Text::new(format!("{}", state.pos[i].2))
                            .set("x", D * (1 + state.pos[i].1) + D / 2)
                            .set("y", S + D * state.pos[i].0 + D / 4)
                            .set("font-size", D / 4)
                            .set("fill", "black"),
                    );
                } else {
                    doc = doc.add(rect(
                        D * (1 + state.pos[i].1),
                        S + D * state.pos[i].0 + D / 4,
                        D,
                        D / 2,
                        &color(state.pos[i].2 as f64 / (input.n * input.n - 1) as f64),
                    ));
                    doc = doc.add(
                        Text::new(format!("{}", state.pos[i].2))
                            .set("x", D * (1 + state.pos[i].1) + D / 2)
                            .set("y", S + D * state.pos[i].0 + D / 2)
                            .set("font-size", D / 4)
                            .set("fill", "black"),
                    );
                }
            }
        }
    }
    (score, err, doc.to_string())
}
