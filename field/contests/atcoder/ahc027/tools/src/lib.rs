#![allow(non_snake_case, unused_macros)]

use itertools::Itertools;
use proconio::{input, marker::Chars};
use rand::prelude::*;
use std::vec;
use svg::node::{
    element::{Circle, Group, Line, Rectangle, Style, Title},
    Text,
};

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

const DIR: &str = "RDLU";
const DIJ: [(usize, usize); 4] = [(0, 1), (1, 0), (0, !0), (!0, 0)];

fn can_move(N: usize, h: &Vec<Vec<char>>, v: &Vec<Vec<char>>, i: usize, j: usize, dir: usize) -> bool {
    let (di, dj) = DIJ[dir];
    let i2 = i + di;
    let j2 = j + dj;
    if i2 >= N || j2 >= N {
        return false;
    }
    if di == 0 {
        v[i][j.min(j2)] == '0'
    } else {
        h[i.min(i2)][j] == '0'
    }
}

#[derive(Clone, Debug)]
pub struct Input {
    pub N: usize,
    pub h: Vec<Vec<char>>,
    pub v: Vec<Vec<char>>,
    pub d: Vec<Vec<i64>>,
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{}", self.N)?;
        for i in 0..self.N - 1 {
            writeln!(f, "{}", self.h[i].iter().collect::<String>())?;
        }
        for i in 0..self.N {
            writeln!(f, "{}", self.v[i].iter().collect::<String>())?;
        }
        for i in 0..self.N {
            writeln!(f, "{}", self.d[i].iter().join(" "))?;
        }
        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let f = proconio::source::once::OnceSource::from(f);
    input! {
        from f,
        N: usize,
        h: [Chars; N - 1],
        v: [Chars; N],
        d: [[i64; N]; N]
    }
    Input { N, h, v, d }
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
        Err("Unexpected EOF".to_owned())
    }
}

pub struct Output {
    pub out: Vec<char>,
}

pub fn parse_output(_input: &Input, f: &str) -> Result<Output, String> {
    let f = f.trim();
    if f.len() > 100000 {
        return Err(format!("Too long route: {}", f.len()));
    }
    Ok(Output {
        out: f.chars().collect(),
    })
}

pub fn gen(seed: u64) -> Input {
    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
    let N = rng.gen_range(20i32..=40) as usize;
    let w = rng.gen_range(1..=N as i32);
    let c = rng.gen_range(1..=N as i32 / 2);
    let (h, v) = loop {
        let mut h = mat!['0'; N - 1; N];
        let mut v = mat!['0'; N; N - 1];
        for _ in 0..w {
            let dir = rng.gen_range(0..4);
            if dir <= 1 {
                let i = rng.gen_range(0..N as i32 - 1) as usize;
                let j = rng.gen_range(0..N as i32) as usize;
                let k = rng.gen_range(3..=N as i32 / 2) as usize;
                for p in 0..k {
                    let j2 = if dir == 0 { j + p } else { j - p };
                    if j2 >= N {
                        break;
                    }
                    h[i][j2] = '1';
                }
            } else {
                let i = rng.gen_range(0..N as i32) as usize;
                let j = rng.gen_range(0..N as i32 - 1) as usize;
                let k = rng.gen_range(3..=N as i32 / 2) as usize;
                for p in 0..k {
                    let i2 = if dir == 0 { i + p } else { i - p };
                    if i2 >= N {
                        break;
                    }
                    v[i2][j] = '1';
                }
            }
        }
        let mut visited = mat![false; N; N];
        let mut stack = vec![(0, 0)];
        visited[0][0] = true;
        let mut count = 0;
        while let Some((i, j)) = stack.pop() {
            count += 1;
            for dir in 0..4 {
                if can_move(N, &h, &v, i, j, dir) {
                    let (di, dj) = DIJ[dir];
                    let i2 = i + di;
                    let j2 = j + dj;
                    if visited[i2][j2].setmax(true) {
                        stack.push((i2, j2));
                    }
                }
            }
        }
        if count == N * N {
            break (h, v);
        }
    };
    let mut d0 = mat![0.0; N; N];
    let mut d = mat![0; N; N];
    let mut chosen = mat![0; N; N];
    for iter in 1..=c {
        let i = rng.gen_range(0..N as i32) as usize;
        let j = rng.gen_range(0..N as i32) as usize;
        let m = rng.gen_range(N as i32..=(N * N) as i32 / c);
        let b = rng.gen_range(0.0..2.0);
        let mut list = vec![(i, j)];
        chosen[i][j] = iter;
        d0[i][j] = b;
        for _ in 1..m {
            loop {
                let &(i, j) = list.choose(&mut rng).unwrap();
                let dir = rng.gen_range(0..4i32) as usize;
                if can_move(N, &h, &v, i, j, dir) {
                    let i2 = i + DIJ[dir].0;
                    let j2 = j + DIJ[dir].1;
                    if chosen[i2][j2].setmax(iter) {
                        list.push((i2, j2));
                        d0[i2][j2] = b;
                        break;
                    }
                }
            }
        }
    }
    for i in 0..N {
        for j in 0..N {
            d[i][j] = f64::powf(10.0, d0[i][j] + rng.gen_range(0.0..1.0)).round() as i64;
        }
    }
    Input { N, h, v, d }
}

pub fn compute_score(input: &Input, out: &Output) -> (i64, String) {
    let ret = evaluate(input, &out.out);
    if ret.err.len() > 0 {
        (0, ret.err)
    } else {
        (ret.score, ret.err)
    }
}

#[derive(Clone, Debug)]
pub struct Eval {
    pub score: i64,
    pub err: String,
    pub d: Vec<Vec<i64>>,
    pub route: Vec<(usize, usize)>,
    pub last_visited: Vec<Vec<usize>>,
    pub edge_count: Vec<Vec<(i32, i32)>>,
    pub S: Vec<i64>,
    pub average: Vec<Vec<f64>>,
}

impl Eval {
    fn get_a(&self, t: usize) -> Vec<Vec<i64>> {
        let N = self.d.len();
        let L = self.route.len() - 1;
        let mut a = mat![0; N; N];
        let mut last_visited2 = self.last_visited.clone();
        for t in L..L + t {
            let (i, j) = self.route[t - L];
            last_visited2[i][j] = t;
        }
        for i in 0..N {
            for j in 0..N {
                a[i][j] = (L + t - last_visited2[i][j]) as i64 * self.d[i][j];
            }
        }
        let (i, j) = self.route[t];
        a[i][j] = 0;
        a
    }
}

pub fn evaluate(input: &Input, out: &[char]) -> Eval {
    let mut last_visited = mat![!0; input.N; input.N];
    let L = out.len();
    let mut i = 0;
    let mut j = 0;
    let mut route = vec![];
    let mut S = vec![];
    let mut average = mat![0.0; input.N; input.N];
    let mut edge_count = mat![(0, 0); input.N; input.N];
    for t in 0..L {
        route.push((i, j));
        last_visited[i][j] = t;
        if let Some(dir) = DIR.find(out[t]) {
            if can_move(input.N, &input.h, &input.v, i, j, dir) {
                if DIJ[dir].0 == 0 {
                    edge_count[i][j.min(j + DIJ[dir].1)].0 += 1;
                } else {
                    edge_count[i.min(i + DIJ[dir].0)][j].1 += 1;
                }
                i += DIJ[dir].0;
                j += DIJ[dir].1;
            } else {
                return Eval {
                    score: 0,
                    err: format!("The output route hits a wall."),
                    d: input.d.clone(),
                    route,
                    last_visited: mat![0; input.N; input.N],
                    S,
                    average,
                    edge_count,
                };
            }
        } else {
            return Eval {
                score: 0,
                err: format!("Illegal output char: {}", out[t]),
                d: input.d.clone(),
                route,
                last_visited: mat![0; input.N; input.N],
                S,
                average,
                edge_count,
            };
        }
    }
    route.push((i, j));
    if (i, j) != (0, 0) {
        return Eval {
            score: 0,
            err: format!("The output route does not return to (0, 0)."),
            d: input.d.clone(),
            route,
            last_visited: mat![0; input.N; input.N],
            S,
            average,
            edge_count,
        };
    }
    for i in 0..input.N {
        for j in 0..input.N {
            if last_visited[i][j] == !0 {
                return Eval {
                    score: 0,
                    err: format!("The output route does not visit ({}, {}).", i, j),
                    d: input.d.clone(),
                    route,
                    last_visited: mat![0; input.N; input.N],
                    S,
                    average,
                    edge_count,
                };
            }
        }
    }
    let mut s = 0;
    let mut sum_d = 0;
    for i in 0..input.N {
        for j in 0..input.N {
            s += (L - last_visited[i][j]) as i64 * input.d[i][j];
            sum_d += input.d[i][j];
        }
    }
    let mut last_visited2 = last_visited.clone();
    let mut sum = mat![0; input.N; input.N];
    for t in L..2 * L {
        let (i, j) = route[t - L];
        let dt = (t - last_visited2[i][j]) as i64;
        let a = dt * input.d[i][j];
        sum[i][j] += dt * (dt - 1) / 2 * input.d[i][j];
        s -= a;
        last_visited2[i][j] = t;
        S.push(s);
        s += sum_d;
    }
    for i in 0..input.N {
        for j in 0..input.N {
            average[i][j] = sum[i][j] as f64 / L as f64;
        }
    }
    let score = (2 * S.iter().sum::<i64>() + L as i64) / (2 * L) as i64;
    Eval {
        score,
        err: String::new(),
        d: input.d.clone(),
        route,
        last_visited,
        S,
        average,
        edge_count,
    }
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
    Group::new().add(Title::new().add(Text::new(title)))
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum VisType {
    A,
    D,
    AvgA,
}

pub fn vis_default(input: &Input, out: &Output) -> (i64, String, String) {
    let (mut score, err, svg) = vis(input, &out.out, 0, VisType::AvgA, -1);
    if err.len() > 0 {
        score = 0;
    }
    (score, err, svg)
}

pub fn vis(input: &Input, out: &[char], t: usize, option: VisType, show_route: i32) -> (i64, String, String) {
    let D = 600 / input.N;
    let ret = evaluate(input, &out);
    let mut doc = svg::Document::new()
        .set("id", "vis")
        .set("viewBox", (-5, -5, D * input.N + 10, D * input.N + 10))
        .set("width", D * input.N + 10)
        .set("height", D * input.N + 10)
        .set("style", "background-color:white");
    doc = doc.add(Style::new(format!(
        "text {{text-anchor: middle;dominant-baseline: central;}}"
    )));
    let t = t.min(ret.route.len() - 1);
    let a = ret.get_a(t);
    for i in 0..input.N {
        for j in 0..input.N {
            let color = match option {
                VisType::A => {
                    if (i, j) == ret.route[t] {
                        "white".to_owned()
                    } else {
                        color((a[i][j] as f64 / 1e2).sqrt() / input.N as f64)
                    }
                }
                VisType::D => color((input.d[i][j] as f64).log10() / 3.0),
                VisType::AvgA => color((ret.average[i][j] as f64 / 1e2).sqrt() / input.N as f64),
            };
            doc = doc.add(
                group(format!(
                    "({}, {})\na = {}\navg_a = {:.0}\nd = {}",
                    i, j, a[i][j], ret.average[i][j], input.d[i][j]
                ))
                .add(rect(j * D, i * D, D, D, &color)),
            );
        }
    }
    for i in 0..=input.N {
        doc = doc
            .add(
                Line::new()
                    .set("x1", 0)
                    .set("y1", i * D)
                    .set("x2", input.N * D)
                    .set("y2", i * D),
            )
            .set("stroke", "gray")
            .set("stroke-width", 1);
        doc = doc
            .add(
                Line::new()
                    .set("x1", i * D)
                    .set("y1", 0)
                    .set("x2", i * D)
                    .set("y2", input.N * D),
            )
            .set("stroke", "gray")
            .set("stroke-width", 1);
    }
    for i in 0..input.N {
        for j in 0..input.N {
            if i + 1 < input.N && input.h[i][j] == '1' {
                doc = doc.add(
                    Line::new()
                        .set("x1", j * D)
                        .set("y1", (i + 1) * D)
                        .set("x2", (j + 1) * D)
                        .set("y2", (i + 1) * D)
                        .set("stroke", "black")
                        .set("stroke-width", 2),
                )
            }
            if j + 1 < input.N && input.v[i][j] == '1' {
                doc = doc.add(
                    Line::new()
                        .set("x1", (j + 1) * D)
                        .set("y1", i * D)
                        .set("x2", (j + 1) * D)
                        .set("y2", (i + 1) * D)
                        .set("stroke", "black")
                        .set("stroke-width", 2),
                )
            }
        }
    }
    if show_route == -1 {
        let L = ret.route.len() - 1;
        for i in 0..input.N {
            for j in 0..input.N {
                if ret.edge_count[i][j].0 > 0 {
                    let c = (ret.edge_count[i][j].0 as f64 / L as f64).sqrt() * input.N as f64 * 0.5;
                    doc = doc.add(
                        Line::new()
                            .set("x1", j * D + D / 2)
                            .set("y1", i * D + D / 2)
                            .set("x2", (j + 1) * D + D / 2)
                            .set("y2", i * D + D / 2)
                            .set("stroke", "lightgray")
                            .set("stroke-width", (D as f64 / 3.0 * c.min(1.0)).max(1.0).round() as i32)
                            .set("stroke-linecap", "round"),
                    )
                }
                if ret.edge_count[i][j].1 > 0 {
                    let c = (ret.edge_count[i][j].1 as f64 / L as f64).sqrt() * input.N as f64 * 0.5;
                    doc = doc.add(
                        Line::new()
                            .set("x1", j * D + D / 2)
                            .set("y1", i * D + D / 2)
                            .set("x2", j * D + D / 2)
                            .set("y2", (i + 1) * D + D / 2)
                            .set("stroke", "lightgray")
                            .set("stroke-width", (D as f64 / 3.0 * c.min(1.0)).max(1.0).round() as i32)
                            .set("stroke-linecap", "round"),
                    )
                }
            }
        }
    } else if show_route > 0 {
        for k in 1..=show_route {
            let mut t = t as i32 - k;
            if t < 0 {
                if ret.err.len() > 0 {
                    break;
                }
                t += ret.route.len() as i32 - 1;
            }
            let (i, j) = ret.route[t as usize];
            let (i2, j2) = ret.route[(t + 1) as usize];
            doc = doc.add(
                Line::new()
                    .set("x1", j * D + D / 2)
                    .set("y1", i * D + D / 2)
                    .set("x2", j2 * D + D / 2)
                    .set("y2", i2 * D + D / 2)
                    .set("stroke", "lightgray")
                    .set("stroke-width", 3)
                    .set("stroke-linecap", "round"),
            )
        }
    }
    if option != VisType::A && t > 0 {
        let (i, j) = ret.route[t];
        doc = doc.add(
            Circle::new()
                .set("cx", j * D + D / 2)
                .set("cy", i * D + D / 2)
                .set("r", D / 3)
                .set("fill", "white")
                .set("stroke", "gray")
                .set("stroke-width", 1),
        );
    }
    (ret.score, ret.err, doc.to_string())
}
