#![allow(non_snake_case, unused_macros)]

use proconio::{input, marker::Bytes};
use rand::prelude::*;
use svg::node::{
    element::{Group, Line, Rectangle, Title},
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
pub struct Output {
    pub n: usize,
    pub b: Vec<Vec<Vec<Vec<usize>>>>,
}

#[derive(Clone, Debug)]
pub struct Input {
    pub D: usize,
    pub f: Vec<Vec<Vec<i32>>>,
    pub r: Vec<Vec<Vec<i32>>>,
}

impl std::fmt::Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{}", self.D)?;
        for i in 0..2 {
            for z in 0..self.D {
                for x in 0..self.D {
                    write!(f, "{}", self.f[i][z][x])?;
                }
                writeln!(f)?;
            }
            for z in 0..self.D {
                for x in 0..self.D {
                    write!(f, "{}", self.r[i][z][x])?;
                }
                writeln!(f)?;
            }
        }
        Ok(())
    }
}

pub fn parse_input(f: &str) -> Input {
    let mut f = proconio::source::once::OnceSource::from(f);
    input! {
        from &mut f,
        D: usize,
    }
    let mut fs = mat![0; 2; D; D];
    let mut rs = mat![0; 2; D; D];
    for i in 0..2 {
        input! {
            from &mut f,
            F: [Bytes; D],
            R: [Bytes; D],
        }
        for z in 0..D {
            for x in 0..D {
                fs[i][z][x] = (F[z][x] - b'0') as i32;
                rs[i][z][x] = (R[z][x] - b'0') as i32;
            }
        }
    }
    Input { D, f: fs, r: rs }
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
    let mut b = mat![0; 2; input.D; input.D; input.D];
    let mut tokens = f.split_whitespace();
    let n = read(tokens.next(), 0, 1000000)?;
    for i in 0..2 {
        for x in 0..input.D {
            for y in 0..input.D {
                for z in 0..input.D {
                    b[i][x][y][z] = read(tokens.next(), 0, n)?;
                }
            }
        }
    }
    if tokens.next().is_some() {
        return Err("Too many outputs".to_owned());
    }
    Ok(Output { n, b })
}

fn normalize(b: &Vec<(usize, usize, usize)>) -> Vec<(usize, usize, usize)> {
    let mut min_x = !0;
    let mut min_y = !0;
    let mut min_z = !0;
    for &(x, y, z) in b {
        min_x.setmin(x);
        min_y.setmin(y);
        min_z.setmin(z);
    }
    b.iter().map(|&(x, y, z)| (x - min_x, y - min_y, z - min_z)).collect()
}

fn is_same(b1: &Vec<(usize, usize, usize)>, b2: &Vec<(usize, usize, usize)>) -> bool {
    if b1.len() != b2.len() {
        return false;
    }
    let mut b1 = normalize(&b1);
    let mut b2 = normalize(&b2);
    let mut max_x = 0;
    let mut max_y = 0;
    let mut max_z = 0;
    for &(x, y, z) in &b2 {
        max_x.setmax(x);
        max_y.setmax(y);
        max_z.setmax(z);
    }
    b1.sort();
    for i in 0..6 {
        for _ in 0..4 {
            b2.sort();
            if b1 == b2 {
                return true;
            }
            for (x, y, _) in &mut b2 {
                let t = *x;
                *x = max_y - *y;
                *y = t;
            }
            std::mem::swap(&mut max_x, &mut max_y);
        }
        if i & 1 != 0 {
            for (_, y, z) in &mut b2 {
                let t = *y;
                *y = max_z - *z;
                *z = t;
            }
            std::mem::swap(&mut max_y, &mut max_z);
        } else {
            for (x, _, z) in &mut b2 {
                let t = *z;
                *z = max_x - *x;
                *x = t;
            }
            std::mem::swap(&mut max_x, &mut max_z);
        }
    }
    false
}

pub const D2: [(usize, usize); 4] = [(0, !0), (0, 1), (!0, 0), (1, 0)];
pub const D3: [(usize, usize, usize); 6] = [(0, 0, !0), (0, 0, 1), (0, !0, 0), (0, 1, 0), (!0, 0, 0), (1, 0, 0)];

pub fn compute_score(input: &Input, out: &Output) -> (i64, String) {
    let mut pos = mat![vec![]; 2; out.n];
    let mut visited = mat![false; 2; input.D; input.D; input.D];
    for i in 0..2 {
        let mut f = mat![0; input.D; input.D];
        let mut r = mat![0; input.D; input.D];
        for x in 0..input.D {
            for y in 0..input.D {
                for z in 0..input.D {
                    let id = out.b[i][x][y][z];
                    if id != 0 {
                        f[z][x] = 1;
                        r[z][y] = 1;
                        pos[i][id - 1].push((x, y, z));
                        if pos[i][id - 1].len() == 1 {
                            visited[i][x][y][z] = true;
                            let mut stack = vec![(x, y, z)];
                            while let Some((x, y, z)) = stack.pop() {
                                for &(dx, dy, dz) in &D3 {
                                    let x2 = x + dx;
                                    let y2 = y + dy;
                                    let z2 = z + dz;
                                    if x2 < input.D
                                        && y2 < input.D
                                        && z2 < input.D
                                        && out.b[i][x2][y2][z2] == id
                                        && !visited[i][x2][y2][z2]
                                    {
                                        visited[i][x2][y2][z2] = true;
                                        stack.push((x2, y2, z2));
                                    }
                                }
                            }
                        } else if !visited[i][x][y][z] {
                            return (0, format!("block {} is not connected in the object {}", id, i + 1));
                        }
                    }
                }
            }
        }
        if f != input.f[i] {
            return (0, format!("The front silhouette for object {} does not match.", i + 1));
        }
        if r != input.r[i] {
            return (0, format!("The right silhouette for object {} does not match.", i + 1));
        }
    }
    let mut sum = 0.0f64;
    for i in 0..out.n {
        if pos[0][i].len() == 0 && pos[1][i].len() == 0 {
            return (0, format!("block {} is not used", i + 1));
        } else if pos[0][i].len() == 0 || pos[1][i].len() == 0 {
            sum += (pos[0][i].len() + pos[1][i].len()) as f64;
        } else if is_same(&pos[0][i], &pos[1][i]) {
            sum += 1.0 / pos[0][i].len() as f64;
        } else {
            return (0, format!("The shape of block {} differs between objects 1 and 2.", i + 1));
        }
    }
    let score = (1e9 * sum).round() as i64;
    (score, String::new())
}

pub fn gen(seed: u64, custom_D: Option<usize>) -> Input {
    if seed == 0 {
        return parse_input(
            r#"5
10001
11011
11111
10101
10001
01110
11011
10000
11011
01110
11110
00011
01110
11000
11111
11110
00011
01110
00011
11110
"#,
        );
    }
    let mut rng = rand_chacha::ChaCha20Rng::seed_from_u64(seed);
    let mut D = rng.gen_range(5i32, 15) as usize;
    if let Some(custom_D) = custom_D {
        D = custom_D;
    }
    let mut f = mat![0; 2; D; D];
    let mut r = mat![0; 2; D; D];
    let mut p = vec![0.0; 5];
    for d in 1..5 {
        p[d] = (D as f64).powf(rng.gen_range(-1.0, 1.0) + if d >= 3 { 0.5 } else { 0.0 });
    }
    for i in 0..4 {
        let g = if i % 2 == 0 { &mut f[i / 2] } else { &mut r[i / 2] };
        loop {
            let num = rng.gen_range(D as i32 * 2, (D * D / 2) as i32 + 1);
            for z in 0..D {
                for x in 0..D {
                    g[z][x] = 0;
                }
            }
            let mut deg = mat![0; D; D];
            for _ in 0..num {
                let mut ws = vec![];
                for z in 0..D {
                    for x in 0..D {
                        if g[z][x] == 0 && deg[z][x] > 0 {
                            ws.push((z, x, p[deg[z][x]]));
                        }
                    }
                }
                let (z, x, _) = if ws.len() > 0 {
                    *ws.choose_weighted(&mut rng, |&(_, _, w)| w).unwrap()
                } else {
                    (rng.gen_range(0, D as i32) as usize, rng.gen_range(0, D as i32) as usize, 0.0)
                };
                g[z][x] = 1;
                for &(dz, dx) in &D2 {
                    let z2 = z + dz;
                    let x2 = x + dx;
                    if z2 < D && x2 < D {
                        deg[z2][x2] += 1;
                    }
                }
            }
            let mut ok = true;
            for z in 0..D {
                ok &= g[z].iter().any(|&v| v == 1);
            }
            if ok {
                break;
            }
        }
    }
    Input { D, f, r }
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

fn rect(x: i32, y: i32, w: i32, h: i32, fill: &str) -> Rectangle {
    Rectangle::new()
        .set("x", x)
        .set("y", y)
        .set("width", w)
        .set("height", h)
        .set("fill", fill)
}

pub fn vis_default(input: &Input, out: &Output) -> String {
    vis(input, out, 1)
}

pub fn vis(input: &Input, out: &Output, color_type: i32) -> String {
    let I = 300 / input.D as i32;
    let W = I * input.D as i32;
    let mut doc = svg::Document::new()
        .set("id", "vis")
        .set("viewBox", (-5, -5, W * 4 + 90, W + 10))
        .set("width", W * 4 + 90)
        .set("height", W + 10);
    doc = doc.add(rect(-5, -5, (W * 4 + 90) as i32, (W + 10) as i32, "white"));
    for i in 1..4 {
        doc = doc.add(
            Line::new()
                .set("x1", (W + 20) * i - 10)
                .set("y1", 0)
                .set("x2", (W + 20) * i - 10)
                .set("y2", W)
                .set("stroke", "gray")
                .set("stroke-width", 1),
        );
    }
    let mut size = mat![0; 2; out.n];
    for i in 0..2 {
        for x in 0..input.D {
            for y in 0..input.D {
                for z in 0..input.D {
                    if out.b[i][x][y][z] > 0 {
                        size[i][out.b[i][x][y][z] - 1] += 1;
                    }
                }
            }
        }
    }
    for i in 0..4 {
        let mut g = mat![0; input.D; input.D];
        for x in 0..input.D {
            for y in 0..input.D {
                for z in 0..input.D {
                    let id = out.b[i / 2][x][y][z];
                    if id > 0 {
                        if i % 2 == 0 {
                            if g[z][x] == 0 {
                                g[z][x] = id;
                            }
                        } else {
                            g[z][y] = id;
                        }
                    }
                }
            }
        }
        for z in 0..input.D {
            for x in 0..input.D {
                if g[z][x] > 0 {
                    doc = doc.add(
                        Group::new()
                            .add(Title::new().add(Text::new(format!(
                                "z = {}, {} = {}, block = {}, size = {}",
                                z,
                                if i % 2 == 0 { "x" } else { "y" },
                                x,
                                g[z][x],
                                size[0][g[z][x] - 1].max(size[1][g[z][x] - 1])
                            ))))
                            .add(rect(
                                (W + 20) * i as i32 + I * x as i32,
                                I * z as i32,
                                I,
                                I,
                                &if color_type == 1 {
                                    color((g[z][x] - 1) as f64 / (out.n - 1).max(1) as f64)
                                } else {
                                    if size[0][g[z][x] - 1] != size[1][g[z][x] - 1] {
                                        "gray".to_owned()
                                    } else {
                                        color((1.0 / size[0][g[z][x] - 1] as f64).sqrt())
                                    }
                                },
                            )),
                    );
                    if z == 0 {
                        doc = doc.add(
                            Line::new()
                                .set("x1", (W + 20) * i as i32 + I * x as i32)
                                .set("y1", I * z as i32)
                                .set("x2", (W + 20) * i as i32 + I * x as i32 + I)
                                .set("y2", I * z as i32)
                                .set("stroke", "black")
                                .set("stroke-width", 2),
                        );
                    }
                    if x == 0 {
                        doc = doc.add(
                            Line::new()
                                .set("x1", (W + 20) * i as i32 + I * x as i32)
                                .set("y1", I * z as i32)
                                .set("x2", (W + 20) * i as i32 + I * x as i32)
                                .set("y2", I * z as i32 + I)
                                .set("stroke", "black")
                                .set("stroke-width", 2),
                        );
                    }
                }
                if g[z][x] > 0 && z + 1 == input.D || z + 1 < input.D && g[z + 1][x] != g[z][x] {
                    doc = doc.add(
                        Line::new()
                            .set("x1", (W + 20) * i as i32 + I * x as i32)
                            .set("y1", I * z as i32 + I)
                            .set("x2", (W + 20) * i as i32 + I * x as i32 + I)
                            .set("y2", I * z as i32 + I)
                            .set("stroke", "black")
                            .set("stroke-width", 2),
                    );
                }
                if g[z][x] > 0 && x + 1 == input.D || x + 1 < input.D && g[z][x + 1] != g[z][x] {
                    doc = doc.add(
                        Line::new()
                            .set("x1", (W + 20) * i as i32 + I * x as i32 + I)
                            .set("y1", I * z as i32)
                            .set("x2", (W + 20) * i as i32 + I * x as i32 + I)
                            .set("y2", I * z as i32 + I)
                            .set("stroke", "black")
                            .set("stroke-width", 2),
                    );
                }
            }
        }
    }
    doc.to_string()
}
