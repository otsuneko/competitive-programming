#![allow(non_snake_case, unused_macros)]

use rand::prelude::*;
use proconio::input;
use svg::node::{element::{Rectangle, Line, Circle, Group, Title}, Text};

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

pub type Output = Vec<(i32, i32, i32, i32)>;

#[derive(Clone, Debug)]
pub struct Input {
	pub N: usize,
	pub K: usize,
	pub xy: Vec<(i32, i32)>,
	pub a: Vec<i32>,
}

impl std::fmt::Display for Input {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		writeln!(f, "{} {}", self.N, self.K)?;
		for d in 0..10 {
			if d > 0 {
				write!(f, " ")?;
			}
			write!(f, "{}", self.a[d])?;
		}
		writeln!(f)?;
		for i in 0..self.N {
			writeln!(f, "{} {}", self.xy[i].0, self.xy[i].1)?;
		}
		Ok(())
	}
}

pub fn parse_input(f: &str) -> Input {
	let f = proconio::source::once::OnceSource::from(f);
	input! {
		from f,
		N: usize, K: usize,
		a: [i32; 10],
		xy: [(i32, i32); N],
	}
	Input { N, K, xy, a }
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

pub fn parse_output(input: &Input, f: &str) -> Result<Vec<Output>, String> {
	let mut out = vec![];
	let mut tokens = f.split_whitespace();
	while let Some(k) = tokens.next() {
		let k = read::<usize>(Some(k), 0, input.K)?;
		let mut pq = vec![];
		for _ in 0..k {
			let px = read(tokens.next(), -1000000000, 1000000000)?;
			let py = read(tokens.next(), -1000000000, 1000000000)?;
			let qx = read(tokens.next(), -1000000000, 1000000000)?;
			let qy = read(tokens.next(), -1000000000, 1000000000)?;
			if (px, py) == (qx, qy) {
				return Err(format!("(px, py) must be different from (qx, qy)"));
			}
			pq.push((px, py, qx, qy));
		}
		out.push(pq);
	}
	Ok(out)
}

pub fn compute_score(input: &Input, out: &Output) -> (i64, String, (Vec<i32>, Vec<Vec<usize>>)) {
	let mut pieces = vec![(0..input.N).collect::<Vec<_>>()];
	for &(px, py, qx, qy) in out {
		let mut new_pieces = vec![];
		for piece in pieces {
			let mut left = vec![];
			let mut right = vec![];
			for j in piece {
				let (x, y) = input.xy[j];
				let side = (qx - px) as i64 * (y - py) as i64 - (qy - py) as i64 * (x - px) as i64;
				if side > 0 {
					left.push(j);
				} else if side < 0 {
					right.push(j);
				}
			}
			if left.len() > 0 {
				new_pieces.push(left);
			}
			if right.len() > 0 {
				new_pieces.push(right);
			}
		}
		pieces = new_pieces;
	}
	let mut b = vec![0; 10];
	for piece in &pieces {
		if piece.len() <= 10 {
			b[piece.len() - 1] += 1;
		}
	}
	let mut num = 0;
	let mut den = 0;
	for d in 0..10 {
		num += input.a[d].min(b[d]);
		den += input.a[d];
	}
	let score = (1e6 * num as f64 / den as f64).round() as i64;
	(score, String::new(), (b, pieces))
}

pub fn gen(seed: u64) -> Input {
	let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
	let mut a = vec![0i32; 10];
	let mut N = 0;
	let K = 100;
	for i in 0..10 {
		a[i] = rng.gen_range(1, 101);
		N += (i + 1) * a[i] as usize;
	}
	let mut xy = vec![];
	for _ in 0..N {
		let p = loop {
			let x = rng.gen_range(-10000, 10001);
			let y = rng.gen_range(-10000, 10001);
			if x * x + y * y < 100000000i32 && xy.iter().all(|(x2, y2)| (x - x2) * (x - x2) + (y - y2) * (y - y2) > 100) {
				break (x, y);
			}
		};
		xy.push(p);
	}
	Input { N, K, xy, a }
}

fn rect(x: i32, y: i32, w: i32, h: i32, fill: &str) -> Rectangle {
	Rectangle::new().set("x", x).set("y", y).set("width", w).set("height", h).set("fill", fill)
}

/// 0 <= val <= 1
fn color(val: f64) -> String {
	let (r, g, b) = if val < 0.5 {
		let x = val * 2.0;
		(30. * (1.0 - x) + 144. * x, 144. * (1.0 - x) + 255. * x, 255. * (1.0 - x) + 30. * x)
	} else {
		let x = val * 2.0 - 1.0;
		(144. * (1.0 - x) + 255. * x, 255. * (1.0 - x) + 30. * x, 30. * (1.0 - x) + 70. * x)
	};
	format!("#{:02x}{:02x}{:02x}", r.round() as i32, g.round() as i32, b.round() as i32)
}

fn intersection_circle_line(c: (f64, f64), r: f64, p: (f64, f64), q: (f64, f64)) -> Option<((f64, f64), (f64, f64))> {
	let vx = q.0 - p.0;
	let vy = q.1 - p.1;
	let mul = (vx * (c.0 - p.0) + vy * (c.1 - p.1)) / (vx * vx + vy * vy);
	let sx = p.0 + vx * mul;
	let sy = p.1 + vy * mul;
	let d = r * r - (sx - c.0) * (sx - c.0) - (sy - c.1) * (sy - c.1);
	if d < 0.0 {
		return None;
	}
	let dx = vx * (d / (vx * vx + vy * vy)).sqrt();
	let dy = vy * (d / (vx * vx + vy * vy)).sqrt();
	Some(((sx - dx, sy - dy), (sx + dx, sy + dy)))
}

pub fn vis(input: &Input, out: &Output) -> (i64, String, String) {
	const H: usize = 120;
	const W: usize = 800;
	let (score, error, (b, pieces)) = compute_score(input, out);
	let mut doc = svg::Document::new().set("id", "vis").set("viewBox", (-5, -5, W + 10, W + H + 10)).set("width", W + 10).set("height", W + H + 10);
	doc = doc.add(rect(-5, -5, (W + 10) as i32, (W + H + 10) as i32, "white"));
	for d in 0..10 {
		doc = doc.add(rect(130 + 60 * d, 10, 60, 30, &color(d as f64 / 9.0)).set("onmouseover", format!("focus_piece({})", d + 1)).set("onmouseleave", format!("unfocus_piece({})", d + 1)));
	}
	for i in 0..4 {
		doc = doc.add(Line::new().set("x1", 70).set("y1", 10 + i * 30).set("x2", 730).set("y2", 10 + i * 30).set("stroke", "black").set("stroke-width", 1));
	}
	for i in 0..12 {
		doc = doc.add(Line::new().set("x1", 70 + 60 * i).set("y1", 10).set("x2", 70 + 60 * i).set("y2", 100).set("stroke", "black").set("stroke-width", 1));
	}
	doc = doc.add(svg::node::element::Text::new().set("x", 100).set("y", 32).set("font-size", 16).set("text-anchor", "middle").add(Text::new("d")));
	doc = doc.add(svg::node::element::Text::new().set("x", 100).set("y", 62).set("font-size", 16).set("text-anchor", "middle").add(Text::new("a")));
	doc = doc.add(svg::node::element::Text::new().set("x", 100).set("y", 92).set("font-size", 16).set("text-anchor", "middle").add(Text::new("b")));
	for d in 0..10 {
		doc = doc.add(svg::node::element::Text::new().set("x", 160 + 60 * d).set("y", 32).set("font-size", 16).set("text-anchor", "middle").add(Text::new(format!("{}", d + 1))));
		doc = doc.add(svg::node::element::Text::new().set("x", 160 + 60 * d).set("y", 62).set("font-size", 16).set("text-anchor", "middle").add(Text::new(format!("{}", input.a[d]))));
		doc = doc.add(svg::node::element::Text::new().set("x", 160 + 60 * d).set("y", 92).set("font-size", 16).set("text-anchor", "middle").add(Text::new(format!("{}", b[d]))));
	}
	doc = doc.add(Circle::new().set("cx", W / 2).set("cy", H + W / 2).set("r", W / 2).set("stroke", "black").set("stroke-width", 2).set("fill", "none"));
	for piece in pieces {
		let color = if piece.len() > 10 {
			"white".to_owned()
		} else {
			color((piece.len() - 1) as f64 / 9.0)
		};
		for &j in &piece {
			doc = doc.add(Group::new()
				.add(Title::new().add(Text::new(format!("({}, {})\nd = {}", input.xy[j].0, input.xy[j].1, piece.len()))))
				.add(Circle::new().set("cx", W as f64 * (input.xy[j].0 + 10000) as f64 / 20000.0).set("cy", H as f64 + W as f64 * (10000 - input.xy[j].1) as f64 / 20000.0).set("r", 4).set("stroke", "gray").set("stroke-width", 1).set("fill", color.clone()).set("class", format!("point piece{}", piece.len()))));
		}
	}
	for &(px, py, qx, qy) in out {
		let title = format!("({}, {}) - ({}, {})", px, py, qx, qy);
		if let Some(((px, py), (qx, qy))) = intersection_circle_line((0.0, 0.0), 10000.0, (px as f64, py as f64), (qx as f64, qy as f64)) {
			doc = doc.add(Group::new()
			.add(Title::new().add(Text::new(title)))
			.add(Line::new().set("x1", W as f64 * (px + 10000.0) / 20000.0).set("y1", H as f64 + W as f64 * (10000.0 - py) / 20000.0).set("x2", W as f64 * (qx + 10000.0) / 20000.0).set("y2", H as f64 + W as f64 * (10000.0 - qy) / 20000.0).set("stroke", "black").set("stroke-width", 1).set("class", "line")));
		}
	}
	(score, error, doc.to_string())
}
