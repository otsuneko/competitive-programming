#![allow(non_snake_case, unused_macros)]

use itertools::Itertools;
use proconio::input;
use rand::prelude::*;
use std::io::prelude::*;
use std::io::BufReader;
use std::process::ChildStdout;
use svg::node::element::Line;
use svg::node::{
    element::{Group, Rectangle, Style, Title},
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

#[derive(Clone, Debug)]
pub struct Input {
    pub n: usize,
    pub m: usize,
    pub eps: f64,
    pub ts: Vec<Vec<(usize, usize)>>,
    pub ps: Vec<(usize, usize)>,
    pub ans: Vec<Vec<i32>>,
    pub es: Vec<f64>,
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{} {} {:.2}", self.n, self.m, self.eps)?;
        for i in 0..self.m {
            writeln!(
                f,
                "{} {}",
                self.ts[i].len(),
                self.ts[i].iter().map(|x| format!("{} {}", x.0, x.1)).join(" ")
            )?;
        }
        for i in 0..self.m {
            writeln!(f, "{} {}", self.ps[i].0, self.ps[i].1)?;
        }
        for i in 0..self.n {
            writeln!(f, "{}", self.ans[i].iter().join(" "))?;
        }
        for i in 0..self.n * self.n * 2 {
            writeln!(f, "{:.10}", self.es[i])?;
        }
        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let f = proconio::source::once::OnceSource::from(f);
    input! {
        from f,
        n: usize, m: usize, eps: f64,
        ts: [[(usize, usize)]; m],
        ps: [(usize, usize); m],
        ans: [[i32; n]; n],
        es: [f64; n * n * 2],
    }
    Input {
        n,
        m,
        eps,
        ts,
        ps,
        ans,
        es,
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
        Err("Unexpected EOF".to_owned())
    }
}

#[derive(Clone, Debug)]
pub enum Query {
    Survey(Vec<(usize, usize)>),
    Mining((usize, usize)),
    Ans(Vec<(usize, usize)>),
}

#[derive(Clone, Debug)]
pub struct Sim {
    pub eps: f64,
    pub ans: Vec<Vec<i32>>,
    pub es: Vec<f64>,
    pub query: Vec<Query>,
    pub resp: Vec<i32>,
    pub cost: f64,
    pub count: usize,
    pub mined: Vec<Vec<usize>>,
    pub finished: bool,
    pub costs: Vec<f64>,
}

impl Sim {
    pub fn new(input: &Input) -> Self {
        let mut count = 0;
        for i in 0..input.n {
            for j in 0..input.n {
                if input.ans[i][j] > 0 {
                    count += 1;
                }
            }
        }
        Self {
            eps: input.eps,
            ans: input.ans.clone(),
            es: input.es.clone(),
            query: vec![],
            resp: vec![],
            cost: 0.0,
            count,
            mined: mat![100000; input.n; input.n],
            finished: false,
            costs: vec![0.0],
        }
    }
    fn query(&mut self, q: Query) -> i32 {
        let resp = match q {
            Query::Mining((x, y)) => {
                self.cost += 1.0;
                self.mined[x][y].setmin(self.resp.len());
                self.ans[x][y]
            }
            Query::Survey(ref ps) => {
                self.cost += 1.0 / (ps.len() as f64).sqrt();
                let mut sum = 0;
                for &(x, y) in ps {
                    sum += self.ans[x][y];
                }
                let k = ps.len() as f64;
                let mu = (k - sum as f64) * self.eps + sum as f64 * (1.0 - self.eps);
                let sigma = (k * self.eps * (1.0 - self.eps)).sqrt();
                ((mu + self.es[self.resp.len()] * sigma).round() as i32).max(0)
            }
            Query::Ans(ref ps) => {
                if ps.len() == self.count && ps.iter().all(|&(x, y)| self.ans[x][y] > 0) {
                    self.finished = true;
                    1
                } else {
                    self.cost += 1.0;
                    0
                }
            }
        };
        self.query.push(q);
        self.resp.push(resp);
        self.costs.push(self.cost);
        resp
    }
}

pub struct Output {
    pub sim: Sim,
    pub comments: Vec<String>,
}

pub fn parse_output(input: &Input, f: &str) -> Result<Output, String> {
    let mut lines = f.lines();
    let mut sim = Sim::new(input);
    let mut comments = vec![];
    let mut comment = String::new();
    while sim.resp.len() < 2 * input.n * input.n {
        let Some(line) = lines.next() else {
            break;
        };
        let line = line.trim();
        if line.starts_with("#") {
            let line = line.trim_start_matches('#').trim();
            comment += line;
            comment.push('\n');
            continue;
        } else if line.is_empty() {
            continue;
        }
        comments.push(comment);
        comment = String::new();
        let mut ss = line.split_whitespace();
        let Some(ty) = ss.next() else {
            return Err(format!("Invalid query format: {}", line));
        };
        let num = read(ss.next(), 1, input.n * input.n)?;
        if ty == "a" {
            let mut ps = vec![];
            for _ in 0..num {
                let x = read(ss.next(), 0, input.n)?;
                let y = read(ss.next(), 0, input.n)?;
                ps.push((x, y));
            }
            ps.sort();
            ps.dedup();
            if ps.len() != num {
                return Err("Query contains the same square multiple times.".to_owned());
            }
            let resp = sim.query(Query::Ans(ps));
            if ss.next().is_some() {
                return Err(format!("Invalid query format: {}", line));
            }
            if resp == 1 {
                break;
            }
        } else if ty == "q" {
            let _resp = if num == 1 {
                sim.query(Query::Mining((read(ss.next(), 0, input.n)?, read(ss.next(), 0, input.n)?)))
            } else {
                let mut ps = vec![];
                for _ in 0..num {
                    let x = read(ss.next(), 0, input.n)?;
                    let y = read(ss.next(), 0, input.n)?;
                    ps.push((x, y));
                }
                ps.sort();
                ps.dedup();
                if ps.len() != num {
                    return Err("Query contains the same square multiple times.".to_owned());
                }
                sim.query(Query::Survey(ps))
            };
            if ss.next().is_some() {
                return Err(format!("Invalid query format: {}", line));
            }
        } else {
            return Err(format!("Invalid query format: {}", line));
        }
    }
    Ok(Output { sim, comments })
}

const DIJ: [(usize, usize); 4] = [(0, 1), (1, 0), (0, !0), (!0, 0)];

pub fn gen(seed: u64, fix_N: Option<usize>, fix_M: Option<usize>, fix_eps: Option<f64>) -> Input {
    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
    let mut n = rng.gen_range(10i32..=20) as usize;
    if let Some(v) = fix_N {
        n = v;
    }
    let mut m = rng.gen_range(2i32..=(n * n / 20) as i32) as usize;
    if let Some(v) = fix_M {
        m = v;
    }
    let mut eps = rng.gen_range(1..=20) as f64 / 100.0;
    if let Some(v) = fix_eps {
        eps = v;
    }
    let avg = (rng.gen_range((n * n / 5) as i32..=(n * n / 2) as i32) as usize / m).max(4);
    let delta = rng.gen_range(0..=avg as i32 - 4) as usize;
    let mut ts = vec![];
    for _ in 0..m {
        let size = rng.gen_range((avg - delta) as i32..=(avg + delta) as i32) as usize;
        let mut used = mat![false; n; n];
        let mut list = vec![];
        list.push((n / 2, n / 2));
        used[n / 2][n / 2] = true;
        let mut adj = vec![];
        for (di, dj) in DIJ {
            let i2 = n / 2 + di;
            let j2 = n / 2 + dj;
            adj.push((i2, j2));
            used[i2][j2] = true;
        }
        while list.len() < size {
            let p = rng.gen_range(0..adj.len() as i32) as usize;
            let (i, j) = adj.remove(p);
            list.push((i, j));
            for (di, dj) in DIJ {
                let i2 = i + di;
                let j2 = j + dj;
                if i2 < n && j2 < n && !used[i2][j2] {
                    adj.push((i2, j2));
                    used[i2][j2] = true;
                }
            }
        }
        let min_i = list.iter().map(|x| x.0).min().unwrap();
        let min_j = list.iter().map(|x| x.1).min().unwrap();
        for x in &mut list {
            x.0 -= min_i;
            x.1 -= min_j;
        }
        list.sort();
        ts.push(list);
    }
    let mut ans = mat![0; n; n];
    let mut ps = vec![];
    for p in 0..m {
        let max_i = ts[p].iter().map(|x| x.0).max().unwrap();
        let max_j = ts[p].iter().map(|x| x.1).max().unwrap();
        let di = rng.gen_range(0..(n - max_i) as i32) as usize;
        let dj = rng.gen_range(0..(n - max_j) as i32) as usize;
        for &(i, j) in &ts[p] {
            ans[i + di][j + dj] += 1;
        }
        ps.push((di, dj));
    }
    let mut es = vec![];
    for _ in 0..n * n * 2 {
        es.push(rng.sample(rand_distr::StandardNormal));
    }
    Input {
        n,
        m,
        eps,
        ts,
        ps,
        ans,
        es,
    }
}

pub fn compute_score(input: &Input, out: &Output) -> (i64, String) {
    let (mut score, err, _) = compute_score_details(input, &out);
    if err.len() > 0 {
        score = 0;
    }
    (score, err)
}

pub fn compute_score_details(input: &Input, out: &Output) -> (i64, String, ()) {
    let mut score = out.sim.cost;
    let mut error = String::new();
    if !out.sim.finished {
        score = 1000.0;
        if out.sim.resp.len() < 2 * input.n * input.n {
            error = "Unexpected EOF".to_owned();
        }
    }
    ((1e6 * score).round() as i64, error, ())
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

pub fn vis_default(input: &Input, out: &Output) -> (i64, String, String) {
    let (mut score, err, svg) = vis(input, &out, out.sim.resp.len(), true);
    if err.len() > 0 {
        score = 0;
    }
    (score, err, svg)
}

pub fn vis(input: &Input, out: &Output, t: usize, show_ans: bool) -> (i64, String, String) {
    let D = 600 / input.n;
    let W = D * input.n;
    let H = D * input.n;
    let (score, err, _) = compute_score_details(input, &out);
    let mut doc = svg::Document::new()
        .set("id", "vis")
        .set("viewBox", (-5, -5, W + 10, H + 10))
        .set("width", W + 10)
        .set("height", H + 10)
        .set("style", "background-color:white");
    doc = doc.add(Style::new(format!(
        "text {{text-anchor: middle;dominant-baseline: central;}}"
    )));
    let mut color = mat!["white"; input.n; input.n];
    for t in 0..t {
        for comment in out.comments[t].lines() {
            if comment.starts_with("c") {
                let ss = comment[1..].trim().split_whitespace().collect::<Vec<_>>();
                if ss.len() == 3 {
                    if let (Ok(i), Ok(j)) = (ss[0].parse::<usize>(), ss[1].parse::<usize>()) {
                        color[i][j] = ss[2];
                    }
                }
            }
        }
    }
    if t > 0 {
        let t = t - 1;
        match out.sim.query[t] {
            Query::Mining((y, x)) => {
                color[y][x] = "tomato";
            }
            Query::Survey(ref ps) => {
                for &(y, x) in ps {
                    color[y][x] = "tomato";
                }
            }
            Query::Ans(ref ps) => {
                for &(y, x) in ps {
                    color[y][x] = "skyblue";
                }
            }
        }
    }
    for i in 0..input.n {
        for j in 0..input.n {
            let mut group = group(format!("({}, {})", i, j)).add(rect(j * D, i * D, D, D, color[i][j]));
            if out.sim.mined[i][j] < t {
                group = group.add(
                    svg::node::element::Text::new()
                        .add(Text::new(format!("{}", out.sim.ans[i][j])))
                        .set("x", (j * D + D / 2) as i32)
                        .set("y", (i * D + D / 2) as i32)
                        .set("font-size", D / 3)
                        .set("fill", "black"),
                );
            } else if show_ans && out.sim.ans[i][j] > 0 {
                group = group.add(
                    svg::node::element::Text::new()
                        .add(Text::new(format!("{}", out.sim.ans[i][j])))
                        .set("x", (j * D + D / 2) as i32)
                        .set("y", (i * D + D / 2) as i32)
                        .set("font-size", D / 3)
                        .set("fill", "darkgray"),
                );
            }
            doc = doc.add(group);
        }
    }
    if show_ans {
        for p in 0..input.m {
            let (di, dj) = input.ps[p];
            let mut inside = mat![false; input.n; input.n];
            for &(i, j) in &input.ts[p] {
                inside[i + di][j + dj] = true;
            }
            for i in 0..input.n {
                for j in 0..input.n {
                    if inside[i][j] {
                        for (di, dj) in DIJ {
                            let i2 = i + di;
                            let j2 = j + dj;
                            if i2 >= input.n || j2 >= input.n || !inside[i2][j2] {
                                let cx = (j * D + D / 2) as i32;
                                let cy = (i * D + D / 2) as i32;
                                let r = (D / 2 - 3) as i32;
                                doc = doc.add(
                                    Line::new()
                                        .set("x1", cx + (dj as i32 - di as i32) * r)
                                        .set("y1", cy + (di as i32 + dj as i32) * r)
                                        .set("x2", cx + (dj as i32 + di as i32) * r)
                                        .set("y2", cy + (di as i32 - dj as i32) * r)
                                        .set("stroke", "green")
                                        .set("stroke-width", 2),
                                );
                            }
                        }
                    }
                }
            }
        }
    }
    for i in 0..=input.n {
        doc = doc.add(
            Line::new()
                .set("x1", 0)
                .set("y1", i * D)
                .set("x2", W)
                .set("y2", i * D)
                .set("stroke", "black")
                .set("stroke-width", 2),
        );
        doc = doc.add(
            Line::new()
                .set("x1", i * D)
                .set("y1", 0)
                .set("x2", i * D)
                .set("y2", W)
                .set("stroke", "black")
                .set("stroke-width", 2),
        );
    }
    (score, err, doc.to_string())
}

fn read_line(stdout: &mut BufReader<ChildStdout>, local: bool) -> Result<String, String> {
    loop {
        let mut out = String::new();
        match stdout.read_line(&mut out) {
            Ok(0) | Err(_) => {
                return Err(format!("Your program has terminated unexpectedly"));
            }
            _ => (),
        }
        if local {
            print!("{}", out);
        }
        let v = out.trim();
        if v.len() == 0 || v.starts_with("#") {
            continue;
        }
        return Ok(v.to_owned());
    }
}

pub fn exec(p: &mut std::process::Child, local: bool) -> Result<i64, String> {
    let mut input = String::new();
    std::io::stdin().read_to_string(&mut input).unwrap();
    let input = parse_input(&input);
    let mut stdin = std::io::BufWriter::new(p.stdin.take().unwrap());
    let mut stdout = std::io::BufReader::new(p.stdout.take().unwrap());
    let _ = writeln!(stdin, "{} {} {:.2}", input.n, input.m, input.eps);
    for i in 0..input.m {
        let _ = writeln!(
            stdin,
            "{} {}",
            input.ts[i].len(),
            input.ts[i].iter().map(|x| format!("{} {}", x.0, x.1)).join(" ")
        );
    }
    let _ = stdin.flush();
    let mut sim = Sim::new(&input);
    for _ in 0..2 * input.n * input.n {
        let line = read_line(&mut stdout, local)?;
        let mut ss = line.split_whitespace();
        let Some(ty) = ss.next() else {
            return Err(format!("Invalid query format: {}", line));
        };
        let num = read(ss.next(), 1, input.n * input.n)?;
        if ty == "a" {
            let mut ps = vec![];
            for _ in 0..num {
                let x = read(ss.next(), 0, input.n)?;
                let y = read(ss.next(), 0, input.n)?;
                ps.push((x, y));
            }
            ps.sort();
            ps.dedup();
            if ps.len() != num {
                return Err("Query contains the same square multiple times.".to_owned());
            }
            let resp = sim.query(Query::Ans(ps));
            if ss.next().is_some() {
                return Err(format!("Invalid query format: {}", line));
            }
            let _ = writeln!(stdin, "{}", resp);
            let _ = stdin.flush();
            if resp == 1 {
                break;
            }
        } else if ty == "q" {
            let resp = if num == 1 {
                sim.query(Query::Mining((read(ss.next(), 0, input.n)?, read(ss.next(), 0, input.n)?)))
            } else {
                let mut ps = vec![];
                for _ in 0..num {
                    let x = read(ss.next(), 0, input.n)?;
                    let y = read(ss.next(), 0, input.n)?;
                    ps.push((x, y));
                }
                ps.sort();
                ps.dedup();
                if ps.len() != num {
                    return Err("Query contains the same square multiple times.".to_owned());
                }
                sim.query(Query::Survey(ps))
            };
            if ss.next().is_some() {
                return Err(format!("Invalid query format: {}", line));
            }
            let _ = writeln!(stdin, "{}", resp);
            let _ = stdin.flush();
        } else {
            return Err(format!("Invalid query format: {}", line));
        }
    }
    p.wait().unwrap();
    Ok(compute_score(&input, &Output { sim, comments: vec![] }).0)
}
