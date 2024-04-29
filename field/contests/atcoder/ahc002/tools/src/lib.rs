#![allow(non_snake_case, dead_code, unused_imports, unused_macros)]

use rand::prelude::*;
use std::io::prelude::*;
use itertools::*;
use proconio::{input, marker::*};
use svg::node::element::{Rectangle, Circle, Path, path::Data};

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

pub const N: usize = 50;
pub type Output = String;

pub struct Input {
	pub s: (usize, usize),
	pub tiles: Vec<Vec<usize>>,
	pub ps: Vec<Vec<i32>>,
}

impl std::fmt::Display for Input {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		writeln!(f, "{} {}", self.s.0, self.s.1)?;
		for i in 0..N {
			writeln!(f, "{}", self.tiles[i].iter().join(" "))?;
		}
		for i in 0..N {
			writeln!(f, "{}", self.ps[i].iter().join(" "))?;
		}
		Ok(())
	}
}

pub fn read_input_str(f: &str) -> Input {
	let f = proconio::source::once::OnceSource::from(f);
	input! {
		from f,
		s: (usize, usize),
		tiles: [[usize; N]; N],
		ps: [[i32; N]; N],
	}
	Input { s, tiles, ps }
}

pub fn read_output_str(_input: &Input, f: &str) -> Output {
	f.trim().to_owned()
}

pub fn compute_score_detail(input: &Input, out: &Output) -> (i32, String, Vec<usize>, Vec<(usize, usize)>) {
	let mut used = vec![0; N * N];
	let (mut i, mut j) = input.s;
	used[input.tiles[i][j]] = 1;
	let mut score = input.ps[i][j];
	let mut steps = vec![(i, j)];
	let mut err = String::new();
	for c in out.chars() {
		let (di, dj) = match c {
			'L' => (0, !0),
			'R' => (0, 1),
			'U' => (!0, 0),
			'D' => (1, 0),
			_ => {
				return (0, "Illegal output".to_owned(), used, steps);
			}
		};
		i += di;
		j += dj;
		if i >= N || j >= N {
			return (0, "Out of range".to_owned(), used, steps);
		}
		steps.push((i, j));
		if used[input.tiles[i][j]] != 0 {
			err = "Stepped on the same tile twice".to_owned();
		}
		used[input.tiles[i][j]] += 1;
		score += input.ps[i][j];
	}
	if err.len() > 0 {
		score = 0;
	}
	(score, err, used, steps)
}

const DIJ: [(usize, usize); 4] = [(0, !0), (0, 1), (!0, 0), (1, 0)];

pub fn gen(seed: u64) -> Input {
	let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
	let s = (rng.gen_range(0, N as u64) as usize, rng.gen_range(0, N as u64) as usize);
	let mut tiles = mat![0; N; N];
	let mut ids = vec![];
	for i in 0..N {
		for j in 0..N {
			ids.push((i, j));
			tiles[i][j] = i * N + j;
		}
	}
	ids.shuffle(&mut rng);
	let mut used = mat![false; N; N];
	for (i, j) in ids {
		if used[i][j] {
			continue;
		}
		let mut dirs = DIJ.iter().cloned().collect::<Vec<_>>();
		dirs.shuffle(&mut rng);
		for (di, dj) in dirs {
			let i2 = i + di;
			let j2 = j + dj;
			if i2 < N && j2 < N && !used[i2][j2] {
				tiles[i2][j2] = tiles[i][j];
				used[i2][j2] = true;
				used[i][j] = true;
				break;
			}
		}
	}
	let mut ids = mat![!0; N * N];
	let mut tn = 0;
	for i in 0..N {
		for j in 0..N {
			if ids[tiles[i][j]] == !0 {
				ids[tiles[i][j]] = tn;
				tn += 1;
			}
		}
	}
	for i in 0..N {
		for j in 0..N {
			tiles[i][j] = ids[tiles[i][j]];
		}
	}
	let mut ps = mat![0; N; N];
	for i in 0..N {
		for j in 0..N {
			ps[i][j] = rng.gen_range(0, 100);
		}
	}
	Input { s, tiles, ps }
}

fn rect(x: usize, y: usize, w: usize, h: usize, fill: &str) -> Rectangle {
	Rectangle::new().set("x", x).set("y", y).set("width", w).set("height", h).set("fill", fill)
}

pub fn vis(input: &Input, out: &Output) -> (i32, String, String) {
	let n = input.tiles.len();
	let m = input.tiles[0].len();
	let (score, err, used, steps) = compute_score_detail(input, out);
	let mut doc = svg::Document::new().set("viewBox", (-1, -1, m * 20 + 2, n * 20 + 2)).set("width", 1002).set("height", 1002);
	doc = doc.add(rect(0, 0, m * 20, n * 20, "white"));
	for i in 0..n {
		for j in 0..m {
			if used[input.tiles[i][j]] == 1 {
				doc = doc.add(rect(j * 20, i * 20, 20, 20, "skyblue"));
			} else if used[input.tiles[i][j]] > 1 {
				doc = doc.add(rect(j * 20, i * 20, 20, 20, "royalblue"));
			}
		}
	}
	let circle = Circle::new().set("cx", input.s.1 * 20 + 10).set("cy", input.s.0 * 20 + 10).set("r", 9).set("fill", "red");
	doc = doc.add(circle);
	let circle = Circle::new().set("cx", steps.last().unwrap().1 * 20 + 10).set("cy", steps.last().unwrap().0 * 20 + 10).set("r", 9).set("fill", "green");
	doc = doc.add(circle);
	doc = doc.add(rect(0, 0, m * 20, n * 20, "none").set("stroke", "black").set("stroke-width", 2));
	for i in 0..n {
		for j in 0..m {
			if i + 1 < n && input.tiles[i][j] != input.tiles[i + 1][j] {
				let data = Data::new().move_to((j * 20, i * 20 + 20)).line_by((20, 0));
				let path = Path::new().set("stroke", "black").set("stroke-width", 2).set("d", data);
				doc = doc.add(path);
			}
			if j + 1 < m && input.tiles[i][j] != input.tiles[i][j + 1] {
				let data = Data::new().move_to((j * 20 + 20, i * 20)).line_by((0, 20));
				let path = Path::new().set("stroke", "black").set("stroke-width", 2).set("d", data);
				doc = doc.add(path);
			}
		}
	}
	let mut data = Data::new().move_to((input.s.1 * 20 + 10, input.s.0 * 20 + 10));
	for p in 1..steps.len() {
		let di = steps[p].0 as i32 - steps[p - 1].0 as i32;
		let dj = steps[p].1 as i32 - steps[p - 1].1 as i32;
		data = data.line_by((dj * 20, di * 20));
	}
	let path = Path::new().set("fill", "none").set("stroke", "orange").set("stroke-width", 4).set("d", data);
	doc = doc.add(path);
	for i in 0..n {
		for j in 0..m {
			doc = doc.add(svg::node::element::Text::new()
					.set("x", j * 20 + 10)
					.set("y", i * 20 + 14).set("font-size", 14)
					.set("text-anchor", "middle")
					.add(svg::node::Text::new(format!("{}", input.ps[i][j]))));
		}
	}
	(score, doc.to_string(), err)
}
