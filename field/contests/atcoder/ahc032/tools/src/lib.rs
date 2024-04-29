#![allow(non_snake_case, unused_macros)]

use itertools::Itertools;
use proconio::input;
use rand::prelude::*;
use std::ops::RangeBounds;
use svg::node::element::{Group, Rectangle, Style, Text, Title};

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

const MOD: i64 = 998244353;

#[derive(Clone, Debug)]
pub struct Input {
    N: usize,
    M: usize,
    K: usize,
    a: Vec<Vec<i64>>,
    s: Vec<Vec<Vec<i64>>>,
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{} {} {}", self.N, self.M, self.K)?;
        for i in 0..self.N {
            writeln!(f, "{}", self.a[i].iter().join(" "))?;
        }
        for i in 0..self.M {
            for j in 0..3 {
                writeln!(f, "{}", self.s[i][j].iter().join(" "))?;
            }
        }
        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let f = proconio::source::once::OnceSource::from(f);
    input! {
        from f,
        N: usize, M: usize, K: usize,
        a: [[i64; N]; N],
        s: [[[i64; 3]; 3]; M],
    }
    Input { N, M, K, a, s }
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
    pub out: Vec<(usize, usize, usize)>,
}

pub fn parse_output(input: &Input, f: &str) -> Result<Output, String> {
    let mut ss = f.split_whitespace();
    let L = read(ss.next(), 0..=input.K)?;
    let mut out = vec![];
    for _ in 0..L {
        let m = read(ss.next(), 0..input.M)?;
        let i = read(ss.next(), 0..=input.N - 3)?;
        let j = read(ss.next(), 0..=input.N - 3)?;
        out.push((m, i, j));
    }
    if ss.next().is_some() {
        return Err(format!("Too many outputs"));
    }
    Ok(Output { out })
}

pub fn gen(seed: u64) -> Input {
    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
    let N = 9;
    let M = 20;
    let K = 81;
    let mut a = mat![0; N; N];
    for i in 0..N {
        for j in 0..N {
            a[i][j] = rng.gen_range(0..MOD);
        }
    }
    let mut s = mat![0; M; 3; 3];
    for i in 0..M {
        for j in 0..3 {
            for k in 0..3 {
                s[i][j][k] = rng.gen_range(0..MOD);
            }
        }
    }
    Input { N, M, K, a, s }
}

pub fn compute_score(input: &Input, out: &Output) -> (i64, String) {
    let (mut score, err, _) = compute_score_details(input, &out.out);
    if err.len() > 0 {
        score = 0;
    }
    (score, err)
}

pub fn compute_score_details(input: &Input, out: &[(usize, usize, usize)]) -> (i64, String, Vec<Vec<i64>>) {
    let mut b = input.a.clone();
    for &(m, i, j) in out {
        for x in 0..3 {
            for y in 0..3 {
                b[i + x][j + y] = (b[i + x][j + y] + input.s[m][x][y]) % MOD;
            }
        }
    }
    let mut score = 0;
    for i in 0..input.N {
        for j in 0..input.N {
            score += b[i][j];
        }
    }
    (score, String::new(), b)
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
    let (mut score, err, svg) = vis(input, &out.out, true);
    if err.len() > 0 {
        score = 0;
    }
    (score, err, svg)
}

pub fn vis(input: &Input, out: &[(usize, usize, usize)], show_number: bool) -> (i64, String, String) {
    let D = 70;
    let W = D * input.N;
    let H = D * input.N;
    let (score, err, b) = compute_score_details(input, &out);
    let mut doc = svg::Document::new()
        .set("id", "vis")
        .set("viewBox", (-5, -5, W + 10, H + 10))
        .set("width", W + 10)
        .set("height", H + 10)
        .set("style", "background-color:white");
    doc = doc.add(Style::new(format!(
        "text {{text-anchor: middle;dominant-baseline: central;}}"
    )));
    for i in 0..input.N {
        for j in 0..input.N {
            let c = 1.0 - (b[i][j] as f64 / MOD as f64).powi(3);
            let mut g = group(format!("b[{},{}] = {}", i, j, b[i][j])).add(rect(j * D, i * D, D, D, &color(c)));
            if show_number {
                g = g.add(
                    Text::new(format!("{:09}", b[i][j]))
                        .set("x", j * D + D / 2)
                        .set("y", i * D + D / 2)
                        .set("font-size", D / 6),
                );
            }
            doc = doc.add(g);
        }
    }
    if out.len() > 0 {
        let (_, i, j) = out[out.len() - 1];
        doc = doc.add(
            rect(j * D, i * D, 3 * D, 3 * D, "none")
                .set("stroke", "black")
                .set("stroke-width", 3),
        );
    }
    (score, err, doc.to_string())
}
