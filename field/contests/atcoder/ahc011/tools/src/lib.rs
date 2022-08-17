#![allow(non_snake_case, unused_macros)]

use rand::prelude::*;
use proconio::{input, marker::*};
use svg::node::{element::{Rectangle, Line, Circle, Group, Title, ClipPath}, Text};

pub trait SetMinMax {
	fn setmin(&mut self, v: Self) -> bool;
	fn setmax(&mut self, v: Self) -> bool;
}
impl<T> SetMinMax for T where T: PartialOrd {
	fn setmin(&mut self, v: T) -> bool {
		*self > v && { *self = v; true }
	}
	fn setmax(&mut self, v: T) -> bool {
		*self < v && { *self = v; true }
	}
}

#[macro_export]
macro_rules! mat {
	($($e:expr),*) => { Vec::from(vec![$($e),*]) };
	($($e:expr,)*) => { Vec::from(vec![$($e),*]) };
	($e:expr; $d:expr) => { Vec::from(vec![$e; $d]) };
	($e:expr; $d:expr $(; $ds:expr)+) => { Vec::from(vec![mat![$e $(; $ds)*]; $d]) };
}

use std::cell::Cell;

#[derive(Clone, Debug)]
pub struct UnionFind {
	/// size / parent
	ps: Vec<Cell<usize>>,
	pub is_root: Vec<bool>
}

impl UnionFind {
	pub fn new(n: usize) -> UnionFind {
		UnionFind { ps: vec![Cell::new(1); n], is_root: vec![true; n] }
	}
	pub fn find(&self, x: usize) -> usize {
		if self.is_root[x] { x }
		else {
			let p = self.find(self.ps[x].get());
			self.ps[x].set(p);
			p
		}
	}
	pub fn unite(&mut self, x: usize, y: usize) {
		let mut x = self.find(x);
		let mut y = self.find(y);
		if x == y { return }
		if self.ps[x].get() < self.ps[y].get() {
			::std::mem::swap(&mut x, &mut y);
		}
		*self.ps[x].get_mut() += self.ps[y].get();
		self.ps[y].set(x);
		self.is_root[y] = false;
	}
	pub fn same(&self, x: usize, y: usize) -> bool {
		self.find(x) == self.find(y)
	}
	pub fn size(&self, x: usize) -> usize {
		self.ps[self.find(x)].get()
	}
}

pub type Output = Vec<char>;

pub const DIJ: [(usize, usize); 4] = [(0, !0), (!0, 0), (0, 1), (1, 0)];
pub const DIR: [char; 4] = ['L', 'U', 'R', 'D'];

#[derive(Clone, Debug)]
pub struct Input {
	pub n: usize,
	pub T: usize,
	pub tiles: Vec<Vec<usize>>,
}

impl std::fmt::Display for Input {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		writeln!(f, "{} {}", self.n, self.T)?;
		for i in 0..self.n {
			for j in 0..self.n {
				write!(f, "{:0x}", self.tiles[i][j])?;
			}
			writeln!(f)?;
		}
		Ok(())
	}
}

pub fn parse_input(f: &str) -> Input {
	let f = proconio::source::once::OnceSource::from(f);
	input! {
		from f,
		n: usize,
		T: usize,
		tiles: [Chars; n]
	}
	let tiles = tiles.iter().map(|ts| ts.iter().map(|&c| usize::from_str_radix(&c.to_string(), 16).unwrap()).collect()).collect();
	Input { n, T, tiles }
}

pub fn parse_output(_input: &Input, f: &str) -> Result<Output, String> {
	Ok(f.trim().chars().collect())
}

pub struct Sim {
	n: usize,
	T: usize,
	from: Vec<Vec<(usize, usize)>>,
	turn: usize,
	i: usize,
	j: usize
}

impl Sim {
	pub fn new(input: &Input) -> Self {
		let mut i = !0;
		let mut j = !0;
		let mut from = mat![(0, 0); input.n; input.n];
		for x in 0..input.n {
			for y in 0..input.n {
				if input.tiles[x][y] == 0 {
					i = x;
					j = y;
				}
				from[x][y] = (x, y);
			}
		}
		Sim {
			n: input.n,
			T: input.T,
			from,
			turn: 0,
			i,
			j
		}
	}
	pub fn apply(&mut self, c: char) -> Result<(), String> {
		if let Some(d) = DIR.iter().position(|&d| d == c) {
			let i2 = self.i + DIJ[d].0;
			let j2 = self.j + DIJ[d].1;
			if i2 >= self.n || j2 >= self.n {
				Err(format!("illegal move: {} (turn {})", c, self.turn))
			} else {
				let f1 = self.from[self.i][self.j];
				let f2 = self.from[i2][j2];
				self.from[i2][j2] = f1;
				self.from[self.i][self.j] = f2;
				self.i = i2;
				self.j = j2;
				self.turn += 1;
				Ok(())
			}
		} else {
			Err(format!("illegal move: {} (turn {})", c, self.turn))
		}
	}
	pub fn compute_score(&self, input: &Input) -> (i64, String, Vec<Vec<bool>>) {
		let mut uf = UnionFind::new(self.n * self.n);
		let mut tree = vec![true; self.n * self.n];
		let mut tiles = mat![0; self.n; self.n];
		for i in 0..self.n {
			for j in 0..self.n {
				tiles[i][j] = input.tiles[self.from[i][j].0][self.from[i][j].1];
			}
		}
		for i in 0..self.n {
			for j in 0..self.n {
				if i + 1 < self.n && tiles[i][j] & 8 != 0 && tiles[i + 1][j] & 2 != 0 {
					let a = uf.find(i * self.n + j);
					let b = uf.find((i + 1) * self.n + j);
					if a == b {
						tree[a] = false;
					} else {
						let t = tree[a] && tree[b];
						uf.unite(a, b);
						tree[uf.find(a)] = t;
					}
				}
				if j + 1 < self.n && tiles[i][j] & 4 != 0 && tiles[i][j + 1] & 1 != 0 {
					let a = uf.find(i * self.n + j);
					let b = uf.find(i * self.n + j + 1);
					if a == b {
						tree[a] = false;
					} else {
						let t = tree[a] && tree[b];
						uf.unite(a, b);
						tree[uf.find(a)] = t;
					}
				}
			}
		}
		let mut max_tree = !0;
		for i in 0..self.n {
			for j in 0..self.n {
				if tiles[i][j] != 0 && tree[uf.find(i * self.n + j)] {
					if max_tree == !0 || uf.size(max_tree) < uf.size(i * self.n + j) {
						max_tree = i * self.n + j;
					}
				}
			}
		}
		let mut bs = mat![false; self.n; self.n];
		if max_tree != !0 {
			for i in 0..self.n {
				for j in 0..self.n {
					bs[i][j] = uf.same(max_tree, i * self.n + j);
				}
			}
		}
		if self.turn > self.T {
			return (0, format!("too many moves"), bs);
		}
		let size = if max_tree == !0 {
			0
		} else {
			uf.size(max_tree)
		};
		let score = if size == self.n * self.n - 1 {
			(500000.0 * (1.0 + (self.T - self.turn) as f64 / self.T as f64)).round()
		} else {
			(500000.0 * size as f64 / (self.n * self.n - 1) as f64).round()
		} as i64;
		(score, String::new(), bs)
	}
}

pub fn compute_score(input: &Input, out: &[char]) -> (i64, String, (Vec<Vec<(usize, usize)>>, Vec<Vec<bool>>)) {
	let mut sim = Sim::new(input);
	for &c in out {
		if let Err(err) = sim.apply(c) {
			return (0, err, (sim.from.clone(), sim.compute_score(input).2));
		}
	}
	let (score, err, tree) = sim.compute_score(input);
	(score, err, (sim.from.clone(), tree))
}

pub fn gen(seed: u64) -> Input {
	let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
	let n = (6 + seed % 5) as usize;
	let T = 2 * n * n * n;
	let mut tiles = mat![0; n; n];
	let mut edges = vec![];
	for i in 0..n {
		for j in 0..n {
			if i + 1 < n && (i + 1, j) != (n - 1, n - 1) {
				edges.push((i, j, i + 1, j));
			}
			if j + 1 < n && (i, j + 1) != (n - 1, n - 1) {
				edges.push((i, j, i, j + 1));
			}
		}
	}
	edges.shuffle(&mut rng);
	let mut uf = UnionFind::new(n * n);
	for (i1, j1, i2, j2) in edges {
		if !uf.same(i1 * n + j1, i2 * n + j2) {
			uf.unite(i1 * n + j1, i2 * n + j2);
			if i1 + 1 == i2 {
				tiles[i1][j1] |= 8;
				tiles[i2][j2] |= 2;
			} else {
				tiles[i1][j1] |= 4;
				tiles[i2][j2] |= 1;
			}
		}
	}
	let mut prev = !0;
	let mut i = n - 1;
	let mut j = n - 1;
	for _ in 0..T {
		let mut dirs = vec![];
		for d in 0..4 {
			if d == prev {
				continue;
			}
			let i2 = i + DIJ[d].0;
			let j2 = j + DIJ[d].1;
			if i2 < n && j2 < n {
				dirs.push(d);
			}
		}
		let d = *dirs.choose(&mut rng).unwrap();
		tiles[i][j] = tiles[i + DIJ[d].0][j + DIJ[d].1];
		tiles[i + DIJ[d].0][j + DIJ[d].1] = 0;
		i += DIJ[d].0;
		j += DIJ[d].1;
		prev = d ^ 2;
	}
	Input { n, T, tiles }
}

fn rect(x: i32, y: i32, w: i32, h: i32, fill: &str) -> Rectangle {
	Rectangle::new().set("x", x).set("y", y).set("width", w).set("height", h).set("fill", fill)
}

pub fn vis(input: &Input, out: &[char], simple: bool) -> (i64, String, String) {
	const W: usize = 80;
	let (score, error, (from, tree)) = compute_score(input, out);
	let mut tiles = mat![0; input.n; input.n];
	for i in 0..input.n {
		for j in 0..input.n {
			tiles[i][j] = input.tiles[from[i][j].0][from[i][j].1];
		}
	}
	let mut doc = svg::Document::new().set("id", "vis").set("viewBox", (-5, -5, W * input.n + 10, W * input.n + 10)).set("width", W * input.n + 10).set("height", W * input.n + 10);
	if !simple {
		doc = doc.add(Text::new(
r#"<filter id="wood" x="-30%" y="-30%" width="160%" height="160%">
<feTurbulence baseFrequency="0.2 0.04" type="fractalNoise"/>
<feColorMatrix values="0 0 0 .8 0 0 0 0 .3 0 0 0 0 .1 0 0 0 0 0 1" result="result1"/>
<feComposite in="result1" in2="SourceGraphic" operator="in" result="result2"/>
<feTurbulence seed="2" type="turbulence" baseFrequency="0.08 0.08" numOctaves="8" result="result3"/>
<feDisplacementMap scale="4" yChannelSelector="G" xChannelSelector="R" in="result2" in2="result3" result="result4"/>
</filter>"#));
	}
	doc = doc.add(rect(-5, -5, (W * input.n + 10) as i32, (W * input.n + 10) as i32, "white"));
	for i in 0..=input.n {
		doc = doc.add(Line::new().set("x1", 0).set("y1", i * W).set("x2", W * input.n).set("y2", i * W).set("stroke", "lightgray").set("stroke-width", 1));
		doc = doc.add(Line::new().set("y1", 0).set("x1", i * W).set("y2", W * input.n).set("x2", i * W).set("stroke", "lightgray").set("stroke-width", 1));
	}
	for i in 0..input.n {
		for j in 0..input.n {
			let color = "#905020";
			let mut g = Group::new().add(Title::new().add(Text::new(format!("({}, {})\ninitial: ({}, {})", i, j, from[i][j].0, from[i][j].1))));
			if tiles[i][j] != 0 {
				let cx = from[i][j].1 * W + W / 2;
				let cy = from[i][j].0 * W + W / 2;
				if simple {
					if tiles[i][j] & 1 != 0 {
						g = g.add(Line::new().set("x1", cx).set("y1", cy).set("x2", cx - W / 2).set("y2", cy).set("stroke", color).set("stroke-width", W / 4));
					}
					if tiles[i][j] & 2 != 0 {
						g = g.add(Line::new().set("x1", cx).set("y1", cy).set("x2", cx).set("y2", cy - W / 2).set("stroke", color).set("stroke-width", W / 4));
					}
					if tiles[i][j] & 4 != 0 {
						g = g.add(Line::new().set("x1", cx).set("y1", cy).set("x2", cx + W / 2).set("y2", cy).set("stroke", color).set("stroke-width", W / 4));
					}
					if tiles[i][j] & 8 != 0 {
						g = g.add(Line::new().set("x1", cx).set("y1", cy).set("x2", cx).set("y2", cy + W / 2).set("stroke", color).set("stroke-width", W / 4));
					}
				} else {
					let cx = cx as i32;
					let cy = cy as i32;
					let w = W as i32;
					let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64((from[i][j].0 * 1000 + from[i][j].1) as u64);
					if tiles[i][j] & 1 != 0 {
						g = g.add(Text::new(format!(r#"<path d="M {} {} Q {} {} {} {} T {} {}" stroke="{}" stroke-width="{}"/>"#, cx, cy, cx - w / 4, rng.gen_range(cy - 12, cy + 13), cx - w / 2, cy, cx - w, cy, color, W / 4)));
					}
					if tiles[i][j] & 2 != 0 {
						g = g.add(Text::new(format!(r#"<path d="M {} {} Q {} {} {} {} T {} {}" stroke="{}" stroke-width="{}"/>"#, cx, cy, rng.gen_range(cx - 12, cx + 13), cy - w / 4, cx, cy - w / 2, cx, cy - w, color, W / 4)));
					}
					if tiles[i][j] & 4 != 0 {
						g = g.add(Text::new(format!(r#"<path d="M {} {} Q {} {} {} {} T {} {}" stroke="{}" stroke-width="{}"/>"#, cx, cy, cx + w / 4, rng.gen_range(cy - 12, cy + 13), cx + w / 2, cy, cx + w, cy, color, W / 4)));
					}
					if tiles[i][j] & 8 != 0 {
						g = g.add(Text::new(format!(r#"<path d="M {} {} Q {} {} {} {} T {} {}" stroke="{}" stroke-width="{}"/>"#, cx, cy, rng.gen_range(cx - 12, cx + 13), cy + w / 4, cx, cy + w / 2, cx, cy + w, color, W / 4)));
					}
				}
				g = g.add(Circle::new().set("cx", cx).set("cy", cy).set("r", W / 8).set("fill", color));
				if !simple {
					g = g.set("filter", "url(#wood)");
				}
				if !tree[i][j] {
					g = g.set("opacity", 0.7);
				}
				g = g.set("transform", format!("translate({},{})", (j * W + W / 2) as i32 - cx as i32, (i * W + W / 2) as i32 - cy as i32));
				if !simple {
					doc = doc.add(ClipPath::new().set("id", format!("clip{}-{}", i, j)).add(Rectangle::new().set("x", from[i][j].1 * W).set("y", from[i][j].0 * W).set("width", W).set("height", W)));
					g = g.set("clip-path", format!("url(#clip{}-{})", i, j));
				}
			} else {
				g = g.add(rect((j * W) as i32, (i * W) as i32, W as i32, W as i32, "lightgray"));
			}
			doc = doc.add(g);
		}
	}
	(score, error, doc.to_string())
}
