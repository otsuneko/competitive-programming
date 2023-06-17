mod seed0;

use itertools::Itertools;
use proconio::{input, marker::Usize1};
use rand::prelude::*;
use rand_chacha::ChaCha20Rng;
use rand_distr::Normal;
use seed0::gen_seed0;
use std::collections::HashSet;
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

pub const MAP_SIZE: i32 = 10000;
pub const MAP_SIZE2: i32 = MAP_SIZE * 2;
pub const MAX_POWER: i32 = 5000;
pub const MIN_BASE_COUNT: i32 = 100;
pub const MAX_BASE_COUNT: i32 = 100;
pub const MIN_BASE_DIST: i32 = 1000;
pub const MIN_HOUSE_COUNT: i32 = 2000;
pub const MAX_HOUSE_COUNT: i32 = 5000;
pub const MIN_PIVOT_COUNT: i32 = 20;
pub const MAX_PIVOT_COUNT: i32 = 40;
pub const MIN_PIVOT_DIST: i32 = 2000;
pub const PIVOT_MAP_SIZE: i32 = 8000;
pub const MIN_STD_DEV: f64 = 200.0;
pub const MAX_STD_DEV: f64 = 1000.0;
pub const MIN_EDGE_COST_COEF: f64 = 10.0;
pub const MAX_EDGE_COST_COEF: f64 = 50.0;

#[derive(Clone, Debug)]
pub struct Input {
    pub n: usize,
    pub m: usize,
    pub k: usize,
    pub stations: Vec<Point>,
    pub edges: Vec<(usize, usize, i32)>,
    pub residents: Vec<Point>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Output {
    pub powers: Vec<i32>,
    pub edges: Vec<bool>,
}

impl Output {
    fn get_broadcasted_count(&self, input: &Input) -> usize {
        let is_connected = self.get_connection_status(input);
        self.get_broadcasted_status(input, &is_connected)
            .iter()
            .filter(|&&b| b)
            .count()
    }

    fn get_connection_status(&self, input: &Input) -> Vec<bool> {
        let mut dsu = Dsu::new(input.n);

        for (j, used) in self.edges.iter().enumerate() {
            if !used {
                continue;
            }

            let (u, v, _) = input.edges[j];
            dsu.merge(u, v);
        }

        (0..input.n).map(|i| dsu.same(0, i)).collect()
    }

    fn get_broadcasted_status(&self, input: &Input, is_connected: &[bool]) -> Vec<bool> {
        let mut broadcasted = vec![false; input.k];

        for i in 0..input.n {
            if !is_connected[i] {
                continue;
            }

            for k in 0..input.k {
                let dist_sq = input.stations[i].calc_sq_dist(&input.residents[k]);
                let power = self.powers[i];
                broadcasted[k] |= dist_sq <= power * power;
            }
        }

        broadcasted
    }

    fn calc_cost(&self, input: &Input) -> i64 {
        let mut cost = 0;

        for i in 0..input.n {
            cost += self.calc_power_cost(i);
        }

        for (j, used) in self.edges.iter().enumerate() {
            if !used {
                continue;
            }

            let (_, _, w) = input.edges[j];
            cost += w as i64;
        }

        cost
    }

    fn calc_power_cost(&self, v: usize) -> i64 {
        let p = self.powers[v] as i64;
        p * p
    }
}

#[derive(Clone, Debug, Copy, PartialEq, Eq, Hash)]
pub struct Point {
    pub x: i32,
    pub y: i32,
}

impl Point {
    pub const fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    pub fn calc_sq_dist(&self, other: &Point) -> i32 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        dx * dx + dy * dy
    }
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{} {} {}", self.n, self.m, self.k)?;
        for p in &self.stations {
            writeln!(f, "{} {}", p.x, p.y)?;
        }

        for &(u, v, w) in &self.edges {
            writeln!(f, "{} {} {}", u + 1, v + 1, w)?;
        }

        for p in &self.residents {
            writeln!(f, "{} {}", p.x, p.y)?;
        }

        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let f = proconio::source::once::OnceSource::from(f);
    input! {
        from f,
        n: usize,
        m: usize,
        k: usize,
        stations: [(i32, i32); n],
        edges: [(Usize1, Usize1, i32); m],
        residents: [(i32, i32); k],
    }

    Input {
        n,
        m,
        k,
        stations: stations.iter().map(|&(x, y)| Point::new(x, y)).collect(),
        edges,
        residents: residents.iter().map(|&(x, y)| Point::new(x, y)).collect(),
    }
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

pub fn parse_output(input: &Input, f: &str) -> Result<Vec<Output>, String> {
    let mut outputs = vec![];
    let mut tokens = f.split_whitespace().peekable();

    while tokens.peek().is_some() {
        let mut powers = vec![];

        for _ in 0..input.n {
            powers.push(read(tokens.next(), 0, MAX_POWER)?);
        }

        let mut edges = vec![];

        for _ in 0..input.m {
            let b = read(tokens.next(), 0, 1)?;
            edges.push(b == 1);
        }

        let output = Output { powers, edges };
        outputs.push(output);
    }

    Ok(outputs)
}

pub fn compute_score(input: &Input, out: &Output) -> (i64, String) {
    let broadcasted_count = out.get_broadcasted_count(&input);

    let score = if broadcasted_count < input.k {
        (1e6 * (broadcasted_count + 1) as f64 / input.k as f64).round() as i64
    } else {
        let cost = out.calc_cost(input);
        (1e6 * (1.0 + 1e8 / (cost as f64 + 1e7))).round() as i64
    };

    (score, String::new())
}

pub fn gen(seed: u64) -> Input {
    if seed == 0 {
        return gen_seed0();
    }

    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);

    loop {
        let mut points_set = HashSet::new();
        let stations = gen_stations(&mut rng, &mut points_set);
        let n = stations.len();

        let edges = gen_edges(&stations, &mut rng);
        let m = edges.len();

        let houses = gen_residents(&mut rng, points_set);
        let k = houses.len();

        if check_reachable(&stations, &houses) {
            return Input {
                n,
                m,
                k,
                residents: houses,
                stations,
                edges,
            };
        }
    }
}

pub fn gen_stations(rng: &mut ChaCha20Rng, points_set: &mut HashSet<Point>) -> Vec<Point> {
    let n = rng.gen_range(MIN_BASE_COUNT, MAX_BASE_COUNT + 1);
    let mut stations = vec![];
    stations.push(Point::new(0, 0));

    for _ in 1..n {
        loop {
            let x = rng.gen_range(-MAP_SIZE, MAP_SIZE + 1);
            let y = rng.gen_range(-MAP_SIZE, MAP_SIZE + 1);

            let point = Point::new(x, y);

            if stations
                .iter()
                .all(|p| p.calc_sq_dist(&point) >= MIN_BASE_DIST * MIN_BASE_DIST)
                && points_set.insert(point)
            {
                stations.push(point);
                break;
            }
        }
    }
    stations
}

pub fn gen_edges(points: &[Point], rng: &mut ChaCha20Rng) -> Vec<(usize, usize, i32)> {
    let points_f64 = points
        .iter()
        .map(|p| delaunator::Point {
            x: p.x as f64,
            y: p.y as f64,
        })
        .collect_vec();
    let triangles = delaunator::triangulate(&points_f64).triangles;
    assert_eq!(triangles.len() % 3, 0);

    let mut edges = vec![];

    for triangle in triangles.chunks(3) {
        for i in 0..3 {
            let u = triangle[i];
            let v = triangle[(i + 1) % 3];
            assert_ne!(u, v);
            edges.push((u.min(v), u.max(v)));
        }
    }

    edges.sort_unstable();
    edges.dedup();

    edges
        .iter()
        .map(|&(u, v)| {
            let dist = (points[u].calc_sq_dist(&points[v]) as f64).sqrt().round();
            let coef = rng.gen_range(MIN_EDGE_COST_COEF, MAX_EDGE_COST_COEF);
            let weight = (coef * coef * dist).round() as i32;
            assert!(100 * dist as i32 <= weight && weight <= 2500 * dist as i32);
            (u, v, weight)
        })
        .collect_vec()
}

pub fn gen_residents(rng: &mut ChaCha20Rng, mut points_set: HashSet<Point>) -> Vec<Point> {
    let k = rng.gen_range(MIN_HOUSE_COUNT, MAX_HOUSE_COUNT + 1);
    let pivot_count = rng.gen_range(MIN_PIVOT_COUNT, MAX_PIVOT_COUNT + 1);
    let mut pivot_centers: Vec<Point> = vec![];

    for _ in 0..pivot_count {
        loop {
            let x = rng.gen_range(-PIVOT_MAP_SIZE, PIVOT_MAP_SIZE + 1);
            let y = rng.gen_range(-PIVOT_MAP_SIZE, PIVOT_MAP_SIZE + 1);

            let pivot = Point::new(x, y);

            if pivot_centers
                .iter()
                .all(|p| p.calc_sq_dist(&pivot) >= MIN_PIVOT_DIST * MIN_PIVOT_DIST)
            {
                pivot_centers.push(pivot);
                break;
            }
        }
    }

    let mut pivot_stddevs = vec![];

    for _ in 0..pivot_count {
        let dev = rng.gen_range(MIN_STD_DEV, MAX_STD_DEV);
        pivot_stddevs.push(dev);
    }

    let mut houses = vec![];

    for _ in 0..k {
        loop {
            let r = rng.gen_range(0, pivot_count) as usize;
            let pivot = pivot_centers[r];
            let std_dev = pivot_stddevs[r];
            let x = Normal::new(pivot.x as f64, std_dev)
                .unwrap()
                .sample(rng)
                .round();
            let y = Normal::new(pivot.y as f64, std_dev)
                .unwrap()
                .sample(rng)
                .round();

            if x.abs() > 1e9 || y.abs() > 1e9 {
                continue;
            }

            let p = Point::new(x as i32, y as i32);

            if p.x.abs() <= MAP_SIZE && p.y.abs() <= MAP_SIZE && points_set.insert(p) {
                houses.push(p);
                break;
            }
        }
    }

    houses
}

pub fn check_reachable(stations: &[Point], residents: &[Point]) -> bool {
    let mut remaining = residents.iter().collect_vec();

    for &station in stations {
        remaining.retain(|p| p.calc_sq_dist(&station) > MAX_POWER * MAX_POWER);
    }

    remaining.len() == 0
}

fn rect(x: i32, y: i32, w: i32, h: i32, fill: &str) -> Rectangle {
    Rectangle::new()
        .set("x", x)
        .set("y", y)
        .set("width", w)
        .set("height", h)
        .set("fill", fill)
}

pub fn vis(input: &Input, out: &Output) -> String {
    fn scale(x: i32) -> f64 {
        W as f64 * x as f64 / MAP_SIZE2 as f64
    }

    fn scale_y(x: i32) -> f64 {
        W as f64 - scale(x)
    }

    const W: i32 = 800;

    let mut doc = svg::Document::new()
        .set("id", "vis")
        .set("viewBox", (-10, -10, W + 20, W + 20))
        .set("width", W + 20)
        .set("height", W + 20);
    doc = doc.add(rect(-10, -10, (W + 20) as i32, (W + 20) as i32, "white"));

    let is_connected = out.get_connection_status(input);
    let is_broadcasted = out.get_broadcasted_status(input, &is_connected);

    for i in 0..input.n {
        if !is_connected[i] {
            continue;
        }

        let cx = scale(input.stations[i].x + MAP_SIZE);
        let cy = scale_y(input.stations[i].y + MAP_SIZE);
        let r = scale(out.powers[i]);
        let circle = Circle::new()
            .set("cx", cx)
            .set("cy", cy)
            .set("r", r)
            .set("fill", "#0151A9")
            .set("fill-opacity", 0.15);
        doc = doc.add(circle);
    }

    for (k, resident) in input.residents.iter().enumerate() {
        let status = if is_broadcasted[k] {
            "broadcasted"
        } else {
            "not broadcasted"
        };
        let title = format!(
            "[resident {}]\nstatus = {}\n({}, {})",
            k + 1,
            status,
            resident.x,
            resident.y
        );
        let title = Title::new().add(Text::new(title));
        let cx = scale(resident.x + MAP_SIZE);
        let cy = scale_y(resident.y + MAP_SIZE);
        let color = if is_broadcasted[k] {
            "lemonchiffon"
        } else {
            "white"
        };

        let circle = Circle::new()
            .set("cx", cx)
            .set("cy", cy)
            .set("r", 4)
            .set("stroke", "gray")
            .set("stoke-width", 1)
            .set("fill", color)
            .set("class", "resident");
        doc = doc.add(Group::new().add(title).add(circle))
    }

    for (j, &used) in out.edges.iter().enumerate() {
        let (u, v, w) = input.edges[j];
        let cost = if used { w } else { 0 };

        let status = if used { "ON" } else { "OFF" };

        let title = format!(
            "[edge {}]\nstatus = {}\nweight = {}\ncost = {}",
            j + 1,
            status,
            w,
            cost
        );

        let title = Title::new().add(Text::new(title));
        let x1 = scale(input.stations[u].x + MAP_SIZE);
        let y1 = scale_y(input.stations[u].y + MAP_SIZE);
        let x2 = scale(input.stations[v].x + MAP_SIZE);
        let y2 = scale_y(input.stations[v].y + MAP_SIZE);
        let width = (w as f64 / (input.stations[u].calc_sq_dist(&input.stations[v]) as f64).sqrt())
            * 4.5
            / (MAX_EDGE_COST_COEF * MAX_EDGE_COST_COEF) as f64
            + 1.5;
        let focused_width = width + 3.0;

        let mut line = Line::new()
            .set("x1", x1)
            .set("y1", y1)
            .set("x2", x2)
            .set("y2", y2)
            .set("stroke", "gray")
            .set("stroke-width", width)
            .set("class", format!("edge{}", j + 1))
            .set(
                "onmouseover",
                format!("set_line({}, {})", j + 1, focused_width),
            )
            .set("onmouseleave", format!("set_line({}, {})", j + 1, width));

        if !used {
            line = line.set("stroke-opacity", 0.1);
        }

        doc = doc.add(Group::new().add(title).add(line));
    }

    for (i, station) in input.stations.iter().enumerate() {
        let status = if is_connected[i] {
            "connected"
        } else {
            "not connected"
        };

        let title = format!(
            "[vertex {}]\nstatus = {}\nstrength = {}\ncost = {}\n({}, {})",
            i + 1,
            status,
            out.powers[i],
            out.calc_power_cost(i),
            station.x,
            station.y
        );

        let title = Title::new().add(Text::new(title));

        const SIZE_SMALL: f64 = 10.0;
        const SIZE_LARGE: f64 = 13.0;
        let x0 = scale(station.x + MAP_SIZE) - SIZE_SMALL / 2.0;
        let y0 = scale_y(station.y + MAP_SIZE) - SIZE_SMALL / 2.0;
        let x1 = scale(station.x + MAP_SIZE) - SIZE_LARGE / 2.0;
        let y1 = scale_y(station.y + MAP_SIZE) - SIZE_LARGE / 2.0;
        let color = if is_connected[i] { "#7AA2CC" } else { "white" };
        let stroke_width = if i == 0 { 2.5 } else { 1.0 };

        let rect = Rectangle::new()
            .set("x", x0)
            .set("y", y0)
            .set("width", SIZE_SMALL)
            .set("height", SIZE_SMALL)
            .set("stroke", "gray")
            .set("stroke-width", stroke_width)
            .set("fill", color)
            .set("class", format!("vertex{}", i + 1))
            .set(
                "onmouseover",
                format!("set_rect({}, {}, {}, {})", i + 1, x1, y1, SIZE_LARGE),
            )
            .set(
                "onmouseleave",
                format!("set_rect({}, {}, {}, {})", i + 1, x0, y0, SIZE_SMALL),
            );
        doc = doc.add(Group::new().add(title).add(rect));
    }

    doc.to_string()
}

pub struct Dsu {
    n: usize,
    parent_or_size: Vec<i32>,
}

impl Dsu {
    pub fn new(size: usize) -> Self {
        Self {
            n: size,
            parent_or_size: vec![-1; size],
        }
    }

    pub fn merge(&mut self, a: usize, b: usize) -> usize {
        assert!(a < self.n);
        assert!(b < self.n);
        let (mut x, mut y) = (self.leader(a), self.leader(b));
        if x == y {
            return x;
        }
        if -self.parent_or_size[x] < -self.parent_or_size[y] {
            std::mem::swap(&mut x, &mut y);
        }
        self.parent_or_size[x] += self.parent_or_size[y];
        self.parent_or_size[y] = x as i32;
        x
    }

    pub fn same(&mut self, a: usize, b: usize) -> bool {
        assert!(a < self.n);
        assert!(b < self.n);
        self.leader(a) == self.leader(b)
    }

    pub fn leader(&mut self, a: usize) -> usize {
        assert!(a < self.n);
        if self.parent_or_size[a] < 0 {
            return a;
        }
        self.parent_or_size[a] = self.leader(self.parent_or_size[a] as usize) as i32;
        self.parent_or_size[a] as usize
    }

    pub fn size(&mut self, a: usize) -> usize {
        assert!(a < self.n);
        let x = self.leader(a);
        -self.parent_or_size[x] as usize
    }

    pub fn groups(&mut self) -> Vec<Vec<usize>> {
        let mut leader_buf = vec![0; self.n];
        let mut group_size = vec![0; self.n];
        for i in 0..self.n {
            leader_buf[i] = self.leader(i);
            group_size[leader_buf[i]] += 1;
        }
        let mut result = vec![Vec::new(); self.n];
        for i in 0..self.n {
            result[i].reserve(group_size[i]);
        }
        for i in 0..self.n {
            result[leader_buf[i]].push(i);
        }
        result
            .into_iter()
            .filter(|x| !x.is_empty())
            .collect::<Vec<Vec<usize>>>()
    }
}
