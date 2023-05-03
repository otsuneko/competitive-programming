#![allow(non_snake_case, unused_macros)]

use delaunator::{triangulate, Point};
use proconio::{input, marker::Usize1};
use rand::prelude::*;
use std::collections::BinaryHeap;
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

pub const INF: i32 = 1000000000;

pub type Output = Vec<usize>;

#[derive(Clone, Debug)]
pub struct Input {
    pub D: usize,
    pub K: usize,
    pub ps: Vec<(i32, i32)>,
    pub es: Vec<(usize, usize, i32)>,
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{} {} {} {}", self.ps.len(), self.es.len(), self.D, self.K)?;
        for &(u, v, w) in &self.es {
            writeln!(f, "{} {} {}", u + 1, v + 1, w)?;
        }
        for p in &self.ps {
            writeln!(f, "{} {}", p.0, p.1)?;
        }
        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let f = proconio::source::once::OnceSource::from(f);
    input! {
        from f,
        N: usize, M: usize, D: usize, K: usize,
        es: [(Usize1, Usize1, i32); M],
        ps: [(i32, i32); N],
    }
    Input { D, K, ps, es }
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

pub fn parse_output(input: &Input, f: &str) -> Result<Output, String> {
    let mut out = vec![];
    let mut tokens = f.split_whitespace();
    for _ in 0..input.es.len() {
        out.push(read(tokens.next(), 1, input.D)?);
    }
    if tokens.next().is_some() {
        return Err("Too many outputs".to_owned());
    }
    Ok(out)
}

fn get_graph(input: &Input, out: &Output, day: usize) -> Vec<Vec<(usize, i32)>> {
    let mut g = vec![vec![]; input.ps.len()];
    for e in 0..input.es.len() {
        if out[e] != day {
            let (u, v, w) = input.es[e];
            g[u].push((v, w));
            g[v].push((u, w));
        }
    }
    g
}

fn compute_dist(g: &Vec<Vec<(usize, i32)>>, s: usize) -> Vec<i32> {
    let mut dist = vec![INF; g.len()];
    let mut que = BinaryHeap::new();
    que.push((0, s));
    dist[s] = 0;
    while let Some((d, u)) = que.pop() {
        let d = -d;
        if dist[u] != d {
            continue;
        }
        for &(v, w) in &g[u] {
            let d2 = d + w;
            if dist[v].setmin(d2) {
                que.push((-d2, v));
            }
        }
    }
    dist
}

fn compute_dist_matrix(input: &Input, out: &Output, day: usize) -> Vec<Vec<i32>> {
    let g = get_graph(input, out, day);
    let mut dist = vec![];
    for s in 0..input.ps.len() {
        dist.push(compute_dist(&g, s));
    }
    dist
}

pub fn compute_score(input: &Input, out: &Output) -> (i64, String, Vec<f64>) {
    let mut count = vec![0; input.D + 1];
    for i in 0..input.es.len() {
        count[out[i]] += 1;
    }
    for i in 1..=input.D {
        if count[i] > input.K {
            return (
                0,
                format!(
                    "The number of edges to be repaired on day {} has exceeded the limit. ({} > {})",
                    i, count[i], input.K
                ),
                vec![],
            );
        }
    }
    let mut num = 0;
    let dist0 = compute_dist_matrix(input, out, !0);
    let mut fs = vec![];
    for day in 1..=input.D {
        let dist = compute_dist_matrix(input, out, day);
        let mut tmp = 0;
        for i in 0..input.ps.len() {
            for j in i + 1..input.ps.len() {
                tmp += (dist[i][j] - dist0[i][j]) as i64;
            }
        }
        num += tmp;
        fs.push(tmp as f64 / (input.ps.len() * (input.ps.len() - 1) / 2) as f64);
    }
    let den = input.D * input.ps.len() * (input.ps.len() - 1) / 2;
    let avg = num as f64 / den as f64 * 1000.0;
    (avg.round() as i64, String::new(), fs)
}

fn dist2((x1, y1): (i32, i32), (x2, y2): (i32, i32)) -> i32 {
    (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
}

pub fn gen(seed: u64) -> Input {
    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed ^ 13);
    let n = rng.gen_range(500i32, 1001) as usize;
    let mut ps = vec![];
    for _ in 0..n {
        loop {
            let p = (rng.gen_range(0, 1001), rng.gen_range(0, 1001));
            if dist2(p, (500, 500)) <= 500 * 500 && ps.iter().all(|&q| dist2(p, q) > 100) {
                ps.push(p);
                break;
            }
        }
    }
    let points = ps
        .iter()
        .map(|&(x, y)| Point {
            x: x as f64,
            y: y as f64,
        })
        .collect::<Vec<_>>();
    let tri = triangulate(&points).triangles;
    assert_eq!(tri.len() % 3, 0);
    let mut es = vec![];
    for i in 0..tri.len() / 3 {
        for j in 0..3 {
            let u = tri[i * 3 + j];
            let v = tri[i * 3 + (j + 1) % 3];
            assert_ne!(u, v);
            es.push((u.min(v), u.max(v)));
        }
    }
    es.sort();
    es.dedup();

    loop {
        let del = rng.gen_range(0.0, 0.75);
        let mut deg = vec![0; n];
        for &(u, v) in &es {
            deg[u] += 1;
            deg[v] += 1;
        }
        let mut shuffled = es.clone();
        shuffled.shuffle(&mut rng);
        let mut es2 = vec![];
        let mut g = Graph::new(n);
        for (u, v) in shuffled {
            if deg[u] > 3 && deg[v] > 3 && rng.gen_bool(del) {
                deg[u] -= 1;
                deg[v] -= 1;
            } else {
                es2.push((u, v));
                g.add(u, v);
            }
        }
        let (id, _) = g.solve();
        if id.iter().all(|&i| i == id[0]) {
            es = es2;
            break;
        }
    }

    let D = rng.gen_range(5i32, 31) as usize;
    let K0 = (es.len() + D - 1) / D;
    let K = rng.gen_range(K0 as i32 + 1, K0 as i32 * 2 + 1) as usize;
    let mut deg = vec![0; n];
    let es = es
        .into_iter()
        .map(|(u, v)| {
            deg[u] += 1;
            deg[v] += 1;
            let w = ((dist2(ps[u], ps[v]) as f64).sqrt() * 1000.0).round() as i32;
            (u, v, w)
        })
        .collect();
    for v in 0..n {
        assert!(deg[v] >= 2);
    }
    Input { D, K, ps, es }
}

/// 0 <= val <= 1
fn color(mut val: f64) -> String {
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

fn rect(x: i32, y: i32, w: i32, h: i32, fill: &str) -> Rectangle {
    Rectangle::new()
        .set("x", x)
        .set("y", y)
        .set("width", w)
        .set("height", h)
        .set("fill", fill)
}

pub fn vis_default(input: &Input, out: &Output) -> String {
    vis(input, out, 0, !0)
}

pub fn vis(input: &Input, out: &Output, day: usize, s: usize) -> String {
    let W = 800;
    let mut doc = svg::Document::new()
        .set("id", "vis")
        .set("viewBox", (-5, -5, W + 10, W + 10))
        .set("width", W + 10)
        .set("height", W + 10);
    doc = doc.add(rect(-5, -5, (W + 10) as i32, (W + 10) as i32, "white"));
    for e in 0..input.es.len() {
        let (u, v, w) = input.es[e];
        let group = Group::new().add(Title::new().add(Text::new(format!(
            "edge {}, w = {}, d = {}",
            e + 1,
            w,
            if out.len() == 0 { -1 } else { out[e] as i32 }
        ))));
        if out.len() > 0 && day == 0 {
            doc = doc.add(
                group.add(
                    Line::new()
                        .set("x1", input.ps[u].0 * W / 1000)
                        .set("y1", W - input.ps[u].1 * W / 1000)
                        .set("x2", input.ps[v].0 * W / 1000)
                        .set("y2", W - input.ps[v].1 * W / 1000)
                        .set("stroke", color((out[e] - 1) as f64 / (input.D - 1) as f64))
                        .set("stroke-width", 3),
                ),
            );
        } else if out.len() > 0 && out[e] == day {
            doc = doc.add(
                group.add(
                    Line::new()
                        .set("x1", input.ps[u].0 * W / 1000)
                        .set("y1", W - input.ps[u].1 * W / 1000)
                        .set("x2", input.ps[v].0 * W / 1000)
                        .set("y2", W - input.ps[v].1 * W / 1000)
                        .set("stroke", "#FF8080")
                        .set("stroke-width", 4),
                ),
            );
        } else {
            doc = doc.add(
                group.add(
                    Line::new()
                        .set("x1", input.ps[u].0 * W / 1000)
                        .set("y1", W - input.ps[u].1 * W / 1000)
                        .set("x2", input.ps[v].0 * W / 1000)
                        .set("y2", W - input.ps[v].1 * W / 1000)
                        .set("stroke", "black")
                        .set("stroke-width", 2),
                ),
            );
        }
    }
    if s != !0 && day > 0 && out.len() > 0 {
        let dist0 = compute_dist(&get_graph(input, out, 0), s);
        let dist1 = compute_dist(&get_graph(input, out, day), s);
        for i in 0..input.ps.len() {
            let d = (((dist1[i] - dist0[i]) as f64).sqrt() * 5e-3).min(1.0);
            doc = doc.add(
                Group::new()
                    .add(Title::new().add(Text::new(format!(
                        "vertex {}, ({}, {}), Δdist = {}",
                        i + 1,
                        input.ps[i].0,
                        input.ps[i].1,
                        dist1[i] - dist0[i]
                    ))))
                    .add(
                        Circle::new()
                            .set("cx", input.ps[i].0 * W / 1000)
                            .set("cy", W - input.ps[i].1 * W / 1000)
                            .set("r", if i == s { 6 } else { 4 })
                            .set(
                                "fill",
                                if i == s {
                                    "purple".to_owned()
                                } else if dist1[i] == INF {
                                    "black".to_owned()
                                } else {
                                    color(d)
                                },
                            )
                            .set("onclick", format!("set_s({})", i)),
                    ),
            );
        }
    } else {
        for i in 0..input.ps.len() {
            doc = doc.add(
                Group::new()
                    .add(Title::new().add(Text::new(format!("vertex {}, ({}, {})", i + 1, input.ps[i].0, input.ps[i].1))))
                    .add(
                        Circle::new()
                            .set("cx", input.ps[i].0 * W / 1000)
                            .set("cy", W - input.ps[i].1 * W / 1000)
                            .set("r", 3)
                            .set("fill", "black")
                            .set("onclick", format!("set_s({})", i)),
                    ),
            );
        }
    }
    doc.to_string()
}

type V = usize;

#[derive(Clone, Debug)]
pub struct Graph {
    pub adj: Vec<Vec<V>>,
}

impl Graph {
    pub fn new(n: usize) -> Graph {
        Graph { adj: vec![vec![]; n] }
    }
    pub fn add(&mut self, u: V, v: V) {
        self.adj[u].push(v);
        self.adj[v].push(u);
    }
    /// Compute ([id; n], [parent; n]).
    /// id[v] := id of the biconnected component containing v.
    /// parent[c] := id of parent of biconnected component c.
    /// parent[r] = !0 when r is a root (when the graph is not connected, there exist multiple roots).
    /// This works even if there exist multiple edges.
    pub fn solve(&self) -> (Vec<V>, Vec<V>) {
        let n = self.adj.len();
        let (parent, preorder) = self.dfs();
        let mut depth = vec![0; n];
        for &v in &preorder {
            if parent[v] != !0 {
                depth[v] = depth[parent[v]] + 1;
            }
        }
        let mut low = depth.clone();
        for &v in preorder.iter().rev() {
            let mut skip = false;
            for &u in &self.adj[v] {
                if u == parent[v] && !skip {
                    skip = true;
                } else {
                    let tmp = low[u];
                    low[v].setmin(tmp);
                }
            }
        }
        let mut ps = vec![!1; n];
        let mut id = vec![0; n];
        for v in preorder {
            if depth[v] == low[v] {
                id[v] = v;
                ps[v] = if parent[v] == !0 { !0 } else { id[parent[v]] }
            } else {
                id[v] = id[parent[v]];
            }
        }
        (id, ps)
    }
    /// ([parent; n], [preorder; n])
    fn dfs(&self) -> (Vec<V>, Vec<V>) {
        let n = self.adj.len();
        let mut parent = vec![!1; n];
        let mut preorder = vec![];
        let mut stack = vec![];
        for r in 0..n {
            if parent[r] == !1 {
                parent[r] = !0;
                preorder.push(r);
                stack.push((r, 0));
                while let Some((u, mut i)) = stack.pop() {
                    while i < self.adj[u].len() {
                        let v = self.adj[u][i];
                        i += 1;
                        if parent[v] == !1 {
                            parent[v] = u;
                            preorder.push(v);
                            stack.push((u, i));
                            stack.push((v, 0));
                            break;
                        }
                    }
                }
            }
        }
        (parent, preorder)
    }
}
