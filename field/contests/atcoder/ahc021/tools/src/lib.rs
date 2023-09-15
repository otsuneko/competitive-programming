#![allow(non_snake_case, unused_macros)]

use itertools::Itertools;
use proconio::input;
use rand::prelude::*;
use svg::node::{
    element::{Circle, Group, Line, Rectangle, Title},
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

const N: usize = 30;
const N2: usize = N * (N + 1) / 2;

pub type Output = Vec<((usize, usize), (usize, usize))>;

#[derive(Clone, Debug)]
pub struct Input {
    pub bs: Vec<Vec<i32>>,
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for i in 0..self.bs.len() {
            writeln!(f, "{}", self.bs[i].iter().join(" "))?;
        }
        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let mut f = proconio::source::once::OnceSource::from(f);
    let mut bs = vec![];
    for i in 0..N {
        input! {
            from &mut f,
            b: [i32; i + 1]
        }
        bs.push(b);
    }
    Input { bs }
}

fn read<T: Copy + PartialOrd + std::fmt::Display + std::str::FromStr>(token: Option<&str>, lb: T, ub: T) -> Result<T, String> {
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

pub fn parse_output(_input: &Input, f: &str) -> Result<Output, String> {
    let mut tokens = f.split_whitespace().peekable();
    let mut out = vec![];
    let len = read(tokens.next(), 0, 10000)?;
    for _ in 0..len {
        let x1 = read(tokens.next(), 0, N - 1)?;
        let y1 = read(tokens.next(), 0, x1)?;
        let x2 = read(tokens.next(), 0, N - 1)?;
        let y2 = read(tokens.next(), 0, x2)?;
        out.push(((x1, y1), (x2, y2)));
    }
    if tokens.next().is_some() {
        return Err("Too many output".to_owned());
    }
    Ok(out)
}

pub fn gen(seed: u64) -> Input {
    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
    let mut list = (0..(N * (N + 1) / 2) as i32).collect::<Vec<_>>();
    list.shuffle(&mut rng);
    let mut bs = vec![vec![]; N];
    for i in 0..N {
        bs[i] = vec![0; i + 1];
        for j in 0..=i {
            bs[i][j] = list.pop().unwrap();
        }
    }
    Input { bs }
}

pub fn compute_score(input: &Input, out: &[((usize, usize), (usize, usize))]) -> (i64, String, Vec<Vec<i32>>) {
    let mut used = vec![vec![]; N];
    for i in 0..N {
        used[i] = vec![false; i + 1];
    }
    let mut bs = input.bs.clone();
    for (t, &(p, q)) in out.iter().enumerate() {
        if !is_adj(p, q) {
            return (
                0,
                format!("({}, {}) and ({}, {}) are not adjacent (turn {})", p.0, p.1, q.0, q.1, t),
                bs,
            );
        }
        let bp = bs[p.0][p.1];
        let bq = bs[q.0][q.1];
        bs[p.0][p.1] = bq;
        bs[q.0][q.1] = bp;
    }
    let mut num = 0;
    for x in 0..N - 1 {
        for y in 0..=x {
            if bs[x][y] > bs[x + 1][y] {
                num += 1;
            }
            if bs[x][y] > bs[x + 1][y + 1] {
                num += 1;
            }
        }
    }
    let score = if num == 0 {
        ((10000 - out.len()) * 5 + 50000) as i64
    } else {
        50000 - num * 50
    };
    (score as i64, String::new(), bs)
}

fn is_adj((x1, y1): (usize, usize), (x2, y2): (usize, usize)) -> bool {
    if x1 == x2 {
        y1 == y2 + 1 || y1 + 1 == y2
    } else if x1 + 1 == x2 {
        y1 == y2 || y1 + 1 == y2
    } else if x1 == x2 + 1 {
        y1 == y2 || y1 == y2 + 1
    } else {
        false
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

pub fn vis_default(input: &Input, out: &[((usize, usize), (usize, usize))]) -> (i64, String, String) {
    vis(input, out, false, -1)
}

pub fn vis(input: &Input, out: &[((usize, usize), (usize, usize))], show_number: bool, focus: i32) -> (i64, String, String) {
    let B = 800 / N / 2 * 2;
    let H = N * (B - 3) + 3;
    let W = N * B;
    let (score, err, bs) = compute_score(input, out);
    let mut doc = svg::Document::new()
        .set("id", "vis")
        .set("viewBox", (-5, -5, W + 10, H + 10))
        .set("width", W + 10)
        .set("height", H + 10)
        .set("style", "background-color:white");
    doc = doc.add(Text::new(
        r#"<defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" 
    refX="3" refY="2" orient="auto">
      <polygon points="0 0, 4 2, 0 4" fill="black"/>
    </marker>
  </defs>"#,
    ));
    for x in 0..N {
        for y in 0..=x {
            let g = bs[x][y];
            doc = doc.add(
                Group::new()
                    .add(Title::new().add(Text::new(format!("b({}, {}) = {}", x, y, g))))
                    .add(
                        Circle::new()
                            .set("cx", B / 2 * (N - 1 - x) + B / 2 + B * y)
                            .set("cy", (B - 3) * x + B / 2)
                            .set("r", B / 2)
                            .set("stroke-width", if focus == g { 3 } else { 1 })
                            .set("stroke", "black")
                            .set("fill", color(bs[x][y] as f64 / N2 as f64))
                            .set("class", "goods")
                            .set("onclick", format!("vis_focus({})", g)),
                    ),
            );
            if show_number {
                doc = doc.add(
                    svg::node::element::Text::new()
                        .set("x", B / 2 * (N - 1 - x) + B / 2 + B * y)
                        .set("y", (B - 3) * x + B / 2 + 4)
                        .set("text-anchor", "middle")
                        .set("font-size", 12)
                        .add(Text::new(g.to_string())),
                )
            }
        }
    }
    if out.len() > 0 {
        let ((x1, y1), (x2, y2)) = out[out.len() - 1];
        doc = doc.add(
            Line::new()
                .set("x1", B / 2 * (N - 1 - x1) + B / 2 + B * y1)
                .set("y1", (B - 3) * x1 + B / 2)
                .set("x2", B / 2 * (N - 1 - x2) + B / 2 + B * y2)
                .set("y2", (B - 3) * x2 + B / 2)
                .set("stroke", "violet")
                .set("stroke-width", 5),
        );
    }
    if focus >= 0 {
        for x in 0..N {
            for y in 0..=x {
                if input.bs[x][y] == focus {
                    let mut x = x;
                    let mut y = y;
                    for &((x1, y1), (x2, y2)) in out {
                        if (x1, y1) == (x, y) {
                            doc = doc.add(
                                Line::new()
                                    .set("x1", B / 2 * (N - 1 - x) + B / 2 + B * y)
                                    .set("y1", (B - 3) * x + B / 2)
                                    .set("x2", B / 2 * (N - 1 - x2) + B / 2 + B * y2)
                                    .set("y2", (B - 3) * x2 + B / 2)
                                    .set("stroke", "black")
                                    .set("stroke-width", 3)
                                    .set("marker-end", "url(#arrowhead)"),
                            );
                            x = x2;
                            y = y2;
                        } else if (x2, y2) == (x, y) {
                            doc = doc.add(
                                Line::new()
                                    .set("x1", B / 2 * (N - 1 - x) + B / 2 + B * y)
                                    .set("y1", (B - 3) * x + B / 2)
                                    .set("x2", B / 2 * (N - 1 - x1) + B / 2 + B * y1)
                                    .set("y2", (B - 3) * x1 + B / 2)
                                    .set("stroke", "black")
                                    .set("stroke-width", 3)
                                    .set("marker-end", "url(#arrowhead)"),
                            );
                            x = x1;
                            y = y1;
                        }
                    }
                }
            }
        }
    }
    (score, err, doc.to_string())
}
