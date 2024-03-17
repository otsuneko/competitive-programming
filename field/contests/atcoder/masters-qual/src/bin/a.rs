#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;
use rustc_hash::FxHashMap;
use rand::prelude::*;

fn main() {
    get_time();
    let input = read_input();
    // precompute(&input);
    solve_sort(input);
    eprintln!("Time = {:.3}", get_time());
}

// 各マスの目標値を焼き鈍しで前計算(これなしだと1250Mくらい)
pub fn precompute(input: &Input) {
    let mut rng = rand_pcg::Pcg64Mcg::seed_from_u64(890482);
    let mut pos = vec![0; input.n2];
    let mut target = (0..input.n2).collect_vec();
    target.shuffle(&mut rng);
    for i in 0..input.n2 {
        pos[target[i]] = i;
    }
    // let weight = (input.n * input.n) as i64;
    let weight = input.n as i64;
    let mut crt = 0;
    for i in 0..input.n2 - 1 {
        crt += weight * input.dist[pos[i]][pos[i + 1]] as i64;
    }
    for i in 0..input.n {
        for j in 0..input.n {
            for dir in 1..=2 {
                if can_move(&input, i, j, dir) {
                    let i2 = i + DIJ[dir].0;
                    let j2 = j + DIJ[dir].1;
                    let d = (target[i * input.n + j] - target[i2 * input.n + j2]) as i64;
                    crt += d * d;
                }
            }
        }
    }
    const T0: f64 = 1.0;
    const T1: f64 = 1e-6;
    let mut temp = T0;
    let mut last = 0.0;
    for iter in 0.. {
        if iter % 1000 == 0 {
            let t = get_time() / 600.0;
            if t >= 1.0 {
                break;
            }
            if last + 0.01 < t {
                last = t;
                eprintln!("{:.02}: {}", t, crt);
                let bk = crt;
                let mut crt = 0;
                for i in 0..input.n2 - 1 {
                    crt += weight * input.dist[pos[i]][pos[i + 1]] as i64;
                }
                for i in 0..input.n {
                    for j in 0..input.n {
                        for dir in 1..=2 {
                            if can_move(&input, i, j, dir) {
                                let i2 = i + DIJ[dir].0;
                                let j2 = j + DIJ[dir].1;
                                let d = (target[i * input.n + j] - target[i2 * input.n + j2]) as i64;
                                crt += d * d;
                            }
                        }
                    }
                }
                assert_eq!(crt, bk);
            }
            temp = T0.powf(1.0 - t) * T1.powf(t) * f64::powi(input.n as f64, 4);
        }
        let i = rng.gen_range(0..input.n2);
        let j = if iter % 2 == 0 {
            rng.gen_range(0..input.n2)
        } else {
            loop {
                let dir = rng.gen_range(0..4);
                if i / input.n + DIJ[dir].0 < input.n && i % input.n + DIJ[dir].1 < input.n {
                    break i + DIJ[dir].0 * input.n + DIJ[dir].1;
                }
            }
        };
        if i == j {
            continue;
        }
        let mut next = crt;
        if target[i] > 0 {
            next -= weight * input.dist[i][pos[target[i] - 1]] as i64;
        }
        if target[i] + 1 < input.n2 {
            next -= weight * input.dist[i][pos[target[i] + 1]] as i64;
        }
        if target[j] > 0 {
            next -= weight * input.dist[j][pos[target[j] - 1]] as i64;
        }
        if target[j] + 1 < input.n2 {
            next -= weight * input.dist[j][pos[target[j] + 1]] as i64;
        }
        for dir in 0..4 {
            if can_move(&input, i / input.n, i % input.n, dir) {
                let i2 = i / input.n + DIJ[dir].0;
                let j2 = i % input.n + DIJ[dir].1;
                let d = (target[i] - target[i2 * input.n + j2]) as i64;
                next -= d * d;
            }
            if can_move(&input, j / input.n, j % input.n, dir) {
                let i2 = j / input.n + DIJ[dir].0;
                let j2 = j % input.n + DIJ[dir].1;
                let d = (target[j] - target[i2 * input.n + j2]) as i64;
                next -= d * d;
            }
        }
        target.swap(i, j);
        pos[target[i]] = i;
        pos[target[j]] = j;
        if target[i] > 0 {
            next += weight * input.dist[i][pos[target[i] - 1]] as i64;
        }
        if target[i] + 1 < input.n2 {
            next += weight * input.dist[i][pos[target[i] + 1]] as i64;
        }
        if target[j] > 0 {
            next += weight * input.dist[j][pos[target[j] - 1]] as i64;
        }
        if target[j] + 1 < input.n2 {
            next += weight * input.dist[j][pos[target[j] + 1]] as i64;
        }
        for dir in 0..4 {
            if can_move(&input, i / input.n, i % input.n, dir) {
                let i2 = i / input.n + DIJ[dir].0;
                let j2 = i % input.n + DIJ[dir].1;
                let d = (target[i] - target[i2 * input.n + j2]) as i64;
                next += d * d;
            }
            if can_move(&input, j / input.n, j % input.n, dir) {
                let i2 = j / input.n + DIJ[dir].0;
                let j2 = j % input.n + DIJ[dir].1;
                let d = (target[j] - target[i2 * input.n + j2]) as i64;
                next += d * d;
            }
        }
        if crt >= next || rng.gen_bool(((crt - next) as f64 / temp).exp()) {
            crt = next;
        } else {
            target.swap(i, j);
            pos[target[i]] = i;
            pos[target[j]] = j;
        }
    }
    eprintln!("{}", pos.iter().join(" "));
    eprintln!("!log cost {}", crt);
}

// クイックソートの要領で再帰的に大きい奴と小さい奴をスワップしていく
fn solve_sort(mut input: Input) {
    let mut rng = rand_pcg::Pcg64Mcg::seed_from_u64(890482);
    let mut crt = vec![(0, input.n2)];
    let mut next = vec![];
    let mut p = (!0, !0);
    let mut q = (!0, !0);
    let mut num = 0;
    // target[i] := i番のマスの値の目標値
    let mut target = vec![0; input.n2];
    // 前計算したデータを使って目標値を設定
    for (u, i) in PRE
        .lines()
        .nth(input.ty as usize)
        .unwrap()
        .split_whitespace()
        .map(|v| v.parse::<usize>().unwrap())
        .enumerate()
    {
        target[i] = u;
    }
    if input.ty == 6 {
        target = (0..input.n2).collect_vec();
    }
    while crt.len() > 0 {
        while let Some((s, t)) = crt.pop() {
            let mid = (s + t) / 2;
            eprintln!("[{}, {})", s, t);
            // 目標値と現在の値を比較することで、スワップすべきマスを列挙
            let mut to_down = vec![];
            let mut to_up = vec![];
            for i in 0..input.n2 {
                if s <= target[i] && target[i] < mid && input.a[i] >= mid as i32 {
                    to_down.push((i / input.n, i % input.n));
                }
                if mid <= target[i] && target[i] < t && input.a[i] < mid as i32 {
                    to_up.push((i / input.n, i % input.n));
                }
            }
            assert_eq!(to_down.len(), to_up.len());
            if to_down.len() == 0 {
                continue;
            }
            assert_eq!(to_down.len(), to_up.len());
            if s + 1 < mid {
                next.push((s, mid));
            }
            if mid + 1 < t {
                next.push((mid, t));
            }
            // スワップしたいマスを全て通る出来るだけ短いパスを計算
            if input.dist.is_empty() {
                // 19番は大きすぎるので貪欲で順番を決定
                if p.0 == !0 {
                    p = to_down[0];
                    q = to_up[0];
                    println!("{} {} {} {}", p.0, p.1, q.0, q.1);
                    num += 1;
                    if num >= 4 * input.n2 {
                        return;
                    }
                }
                let mut sums = vec![0; 2];
                for _ in 0..to_down.len() {
                    let mut dist = mat![(1000000, !0); input.n2];
                    let mut trace = Trace::new();
                    dist[p.0 * input.n + p.1] = (0, !0);
                    let mut que = VecDeque::new();
                    que.push_back(p);
                    let mut mv1 = vec![];
                    while let Some(u) = que.pop_front() {
                        let (d, id) = dist[u.0 * input.n + u.1];
                        let uij = u.0 * input.n + u.1;
                        if s <= target[uij] && target[uij] < mid && input.a[uij] >= mid as i32 {
                            p = u;
                            mv1 = trace.get(id);
                            break;
                        }
                        for dir in 0..4 {
                            let v = (u.0 + DIJ[dir].0, u.1 + DIJ[dir].1);
                            if can_move(&input, u.0, u.1, dir) && dist[v.0 * input.n + v.1].0 > d + 1 {
                                dist[v.0 * input.n + v.1] = (d + 1, trace.add(DIRS[dir], id));
                                que.push_back(v);
                            }
                        }
                    }
                    let mut dist = mat![(1000000, !0); input.n2];
                    let mut trace = Trace::new();
                    dist[q.0 * input.n + q.1] = (0, !0);
                    let mut que = VecDeque::new();
                    que.push_back(q);
                    let mut mv2 = vec![];
                    while let Some(u) = que.pop_front() {
                        let (d, id) = dist[u.0 * input.n + u.1];
                        let uij = u.0 * input.n + u.1;
                        if mid <= target[uij] && target[uij] < t && input.a[uij] < mid as i32 {
                            q = u;
                            mv2 = trace.get(id);
                            break;
                        }
                        for dir in 0..4 {
                            let v = (u.0 + DIJ[dir].0, u.1 + DIJ[dir].1);
                            if can_move(&input, u.0, u.1, dir) && dist[v.0 * input.n + v.1].0 > d + 1 {
                                dist[v.0 * input.n + v.1] = (d + 1, trace.add(DIRS[dir], id));
                                que.push_back(v);
                            }
                        }
                    }
                    sums[0] += mv1.len();
                    sums[1] += mv2.len();
                    for i in 0..mv1.len().min(mv2.len()) {
                        println!("{} {} {}", if i > 0 { 0 } else { 1 }, mv1[i], mv2[i]);
                        num += 1;
                        if num >= 4 * input.n2 {
                            return;
                        }
                    }
                    for i in mv1.len().min(mv2.len())..mv1.len() {
                        println!("{} {} {}", if i > 0 { 0 } else { 1 }, mv1[i], '.');
                        num += 1;
                        if num >= 4 * input.n2 {
                            return;
                        }
                    }
                    for i in mv1.len().min(mv2.len())..mv2.len() {
                        println!("{} {} {}", if i > 0 { 0 } else { 1 }, '.', mv2[i]);
                        num += 1;
                        if num >= 4 * input.n2 {
                            return;
                        }
                    }
                    input.a.swap(p.0 * input.n + p.1, q.0 * input.n + q.1);
                }
                dbg!(sums);
            } else {
                // TSPソルバに投げる
                let mut routes = vec![];
                for iter in 0..2 {
                    let to = if iter == 0 { &to_down } else { &to_up };
                    let u = if iter == 0 { p } else { q };
                    let mut g = mat![0; to.len() + 2; to.len() + 2];
                    for i in 0..to.len() {
                        for j in 0..to.len() {
                            g[2 + i][2 + j] = input.dist[to[i].0 * input.n + to[i].1][to[j].0 * input.n + to[j].1];
                        }
                        if u.0 == !0 {
                            g[0][2 + i] = 1000;
                            g[2 + i][0] = 1000;
                        } else {
                            g[0][2 + i] = input.dist[u.0 * input.n + u.1][to[i].0 * input.n + to[i].1];
                            g[2 + i][0] = g[0][2 + i];
                        }
                        g[1][2 + i] = 1000;
                        g[2 + i][1] = 1000;
                    }
                    let mut route = tsp::solve(
                        &g,
                        &tsp::greedy(&g),
                        get_time() + 0.3 * ((t - s) as f64 / (input.n2) as f64).powf(2.0),
                        &mut rng,
                    );
                    if route[1] == 1 {
                        route.reverse();
                    }
                    routes.push(route[1..route.len() - 2].iter().map(|&v| to[v - 2]).collect_vec());
                }
                if p.0 == !0 {
                    p = routes[0][0];
                    q = routes[1][0];
                    println!("{} {} {} {}", p.0, p.1, q.0, q.1);
                }
                for k in 0..to_down.len() {
                    let mv1 = get_moves(&input, p, routes[0][k]);
                    let mv2 = get_moves(&input, q, routes[1][k]);
                    for i in 0..mv1.len().min(mv2.len()) {
                        println!("{} {} {}", if i > 0 { 0 } else { 1 }, mv1[i], mv2[i]);
                        num += 1;
                        if num >= 4 * input.n2 {
                            return;
                        }
                    }
                    for i in mv1.len().min(mv2.len())..mv1.len() {
                        println!("{} {} {}", if i > 0 { 0 } else { 1 }, mv1[i], '.');
                        num += 1;
                        if num >= 4 * input.n2 {
                            return;
                        }
                    }
                    for i in mv1.len().min(mv2.len())..mv2.len() {
                        println!("{} {} {}", if i > 0 { 0 } else { 1 }, '.', mv2[i]);
                        num += 1;
                        if num >= 4 * input.n2 {
                            return;
                        }
                    }
                    p = routes[0][k];
                    q = routes[1][k];
                    input.a.swap(p.0 * input.n + p.1, q.0 * input.n + q.1);
                }
            }
        }
        crt = next;
        crt.sort_by_key(|a| a.0);
        if p.0 + q.0 < input.n {
            crt.reverse();
        }
        next = vec![];
    }
}

fn get_moves(input: &Input, mut s: (usize, usize), t: (usize, usize)) -> Vec<char> {
    let mut out = vec![];
    while s != t {
        let mut next = !0;
        for dir in 0..4 {
            if can_move(input, s.0, s.1, dir)
                && input.dist[s.0 * input.n + s.1][t.0 * input.n + t.1]
                    == input.dist[(s.0 + DIJ[dir].0) * input.n + s.1 + DIJ[dir].1][t.0 * input.n + t.1] + 1
            {
                next = dir;
                break;
            }
        }
        out.push(DIRS[next]);
        s.0 += DIJ[next].0;
        s.1 += DIJ[next].1;
    }
    out
}

// 入出力と得点計算

#[derive(Clone, Debug)]
pub struct Input {
    ty: u64,
    n: usize,
    n2: usize,
    a: Vec<i32>,
    vs: Vec<Vec<char>>,
    hs: Vec<Vec<char>>,
    dist: Vec<Vec<i32>>,
}

pub fn read_input() -> Input {
    input! {
        ty: u64, n: usize,
        vs: [Chars; n],
        hs: [Chars; n - 1],
        a: [[i32; n]; n],
    }
    let a = a.into_iter().flatten().map(|v| v - 1).collect_vec();
    let mut input = Input {
        ty,
        n,
        n2: n * n,
        a,
        vs,
        hs,
        dist: vec![],
    };
    if input.n <= 50 {
        let mut dist = mat![i32::max_value(); n * n; n * n];
        for s in 0..n * n {
            dist[s][s] = 0;
            let mut que = VecDeque::new();
            que.push_back(s);
            while let Some(u) = que.pop_front() {
                let d = dist[s][u];
                for dir in 0..4 {
                    if can_move(&input, u / input.n, u % input.n, dir) {
                        let v = u + DIJ[dir].0 * input.n + DIJ[dir].1;
                        if dist[s][v].setmin(d + 1) {
                            que.push_back(v);
                        }
                    }
                }
            }
        }
        input.dist = dist;
    }
    input
}

const DIRS: [char; 5] = ['U', 'D', 'L', 'R', '.'];
const DIJ: [(usize, usize); 5] = [(!0, 0), (1, 0), (0, !0), (0, 1), (0, 0)];

fn can_move(input: &Input, i: usize, j: usize, dir: usize) -> bool {
    let (di, dj) = DIJ[dir];
    let i2 = i + di;
    let j2 = j + dj;
    if i2 >= input.n || j2 >= input.n {
        return false;
    }
    if di == 0 {
        input.vs[i][j.min(j2)] == '0'
    } else {
        input.hs[i.min(i2)][j] == '0'
    }
}

// ここからライブラリ

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
	($($e:expr),*) => { vec![$($e),*] };
	($($e:expr,)*) => { vec![$($e),*] };
	($e:expr; $d:expr) => { vec![$e; $d] };
	($e:expr; $d:expr $(; $ds:expr)+) => { vec![mat![$e $(; $ds)*]; $d] };
}

pub fn get_time() -> f64 {
    static mut STIME: f64 = -1.0;
    let t = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap();
    let ms = t.as_secs() as f64 + t.subsec_nanos() as f64 * 1e-9;
    unsafe {
        if STIME < 0.0 {
            STIME = ms;
        }
        // ローカル環境とジャッジ環境の実行速度差はget_timeで吸収しておくと便利
        #[cfg(feature = "local")]
        {
            (ms - STIME) * 1.0
        }
        #[cfg(not(feature = "local"))]
        {
            ms - STIME
        }
    }
}

pub struct Trace<T: Copy> {
    log: Vec<(T, usize)>,
}

impl<T: Copy> Trace<T> {
    pub fn new() -> Self {
        Trace { log: vec![] }
    }
    pub fn add(&mut self, c: T, p: usize) -> usize {
        self.log.push((c, p));
        self.log.len() - 1
    }
    pub fn get(&self, mut i: usize) -> Vec<T> {
        let mut out = vec![];
        while i != !0 {
            out.push(self.log[i].0);
            i = self.log[i].1;
        }
        out.reverse();
        out
    }
}

mod tsp {

    use super::*;
    use rand_pcg::Pcg64Mcg;
    type C = i32;

    pub fn compute_cost(g: &Vec<Vec<C>>, ps: &Vec<usize>) -> C {
        let mut tmp = 0;
        for i in 0..ps.len() - 1 {
            tmp += g[ps[i]][ps[i + 1]];
        }
        tmp
    }

    pub fn greedy(g: &Vec<Vec<C>>) -> Vec<usize> {
        let mut ps = vec![0];
        let n = g.len();
        let mut used = vec![false; n];
        used[0] = true;
        for i in 0..n - 1 {
            let mut to = !0;
            let mut cost = C::max_value();
            for j in 0..n {
                if !used[j] && cost.setmin(g[i][j]) {
                    to = j;
                }
            }
            used[to] = true;
            ps.push(to);
        }
        ps.push(0);
        ps
    }

    // mv: (i, dir)
    pub fn apply_move(tour: &mut Vec<usize>, idx: &mut Vec<usize>, mv: &[(usize, usize)]) {
        let k = mv.len();
        let mut ids: Vec<_> = (0..k).collect();
        ids.sort_by_key(|&i| mv[i].0);
        let mut order = vec![0; k];
        for i in 0..k {
            order[ids[i]] = i;
        }
        let mut tour2 = Vec::with_capacity(mv[ids[k - 1]].0 - mv[ids[0]].0);
        let mut i = ids[0];
        let mut dir = 0;
        loop {
            let (j, rev) = if dir == mv[i].1 {
                ((i + 1) % k, 0)
            } else {
                ((i + k - 1) % k, 1)
            };
            if mv[j].1 == rev {
                if order[j] == k - 1 {
                    break;
                } else {
                    i = ids[order[j] + 1];
                    dir = 0;
                    tour2.extend_from_slice(&tour[mv[j].0 + 1..mv[i].0 + 1]);
                }
            } else {
                i = ids[order[j] - 1];
                dir = 1;
                tour2.extend(tour[mv[i].0 + 1..mv[j].0 + 1].iter().rev().cloned());
            }
        }
        assert_eq!(tour2.len(), mv[ids[k - 1]].0 - mv[ids[0]].0);
        tour[mv[ids[0]].0 + 1..mv[ids[k - 1]].0 + 1].copy_from_slice(&tour2);
        for i in mv[ids[0]].0 + 1..mv[ids[k - 1]].0 + 1 {
            idx[tour[i]] = i;
        }
    }

    pub const FEASIBLE3: [bool; 64] = [
        false, false, false, true, false, true, true, true, true, true, true, false, true, false, false, false, false, false,
        false, false, false, false, false, false, false, false, false, true, false, true, true, true, true, true, true, false,
        true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, true, false,
        true, true, true, true, true, true, false, true, false, false, false,
    ];

    pub fn solve(g: &Vec<Vec<C>>, qs: &Vec<usize>, until: f64, rng: &mut Pcg64Mcg) -> Vec<usize> {
        let n = g.len();
        let mut f = vec![vec![]; n];
        for i in 0..n {
            for j in 0..n {
                if i != j {
                    f[i].push((g[i][j], j));
                }
            }
            f[i].sort_by(|&(a, _), &(b, _)| a.partial_cmp(&b).unwrap());
        }
        let mut ps = qs.clone();
        let mut idx = vec![!0; n];
        let (mut min, mut min_ps) = (compute_cost(&g, &qs), ps.clone());
        while get_time() < until {
            let mut cost = compute_cost(&g, &ps);
            for p in 0..n {
                idx[ps[p]] = p;
            }
            loop {
                let mut ok = false;
                for i in 0..n {
                    for di in 0..2 {
                        'loop_ij: for &(ij, vj) in &f[ps[i + di]] {
                            if g[ps[i]][ps[i + 1]] - ij <= 0 {
                                break;
                            }
                            for dj in 0..2 {
                                let j = if idx[vj] == 0 && dj == 0 { n - 1 } else { idx[vj] - 1 + dj };
                                let gain = g[ps[i]][ps[i + 1]] - ij + g[ps[j]][ps[j + 1]];
                                // 2-opt
                                if di != dj && gain - g[ps[j + dj]][ps[i + 1 - di]] > 0 {
                                    cost -= gain - g[ps[j + dj]][ps[i + 1 - di]];
                                    apply_move(&mut ps, &mut idx, &[(i, di), (j, dj)]);
                                    ok = true;
                                    break 'loop_ij;
                                }
                                // 3-opt
                                for &(jk, vk) in &f[ps[j + dj]] {
                                    if gain - jk <= 0 {
                                        break;
                                    }
                                    for dk in 0..2 {
                                        let k = if idx[vk] == 0 && dk == 0 { n - 1 } else { idx[vk] - 1 + dk };
                                        if i == k || j == k {
                                            continue;
                                        }
                                        let gain = gain - jk + g[ps[k]][ps[k + 1]];
                                        if gain - g[ps[k + dk]][ps[i + 1 - di]] > 0 {
                                            let mask = if i < j { 1 << 5 } else { 0 }
                                                | if i < k { 1 << 4 } else { 0 }
                                                | if j < k { 1 << 3 } else { 0 }
                                                | di << 2
                                                | dj << 1
                                                | dk;
                                            if FEASIBLE3[mask] {
                                                cost -= gain - g[ps[k + dk]][ps[i + 1 - di]];
                                                apply_move(&mut ps, &mut idx, &[(i, di), (j, dj), (k, dk)]);
                                                ok = true;
                                                break 'loop_ij;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                if !ok {
                    break;
                }
            }
            if min.setmin(cost) {
                min_ps = ps;
            }
            ps = min_ps.clone();
            if n <= 4 {
                break;
            }
            loop {
                if rng.gen_range(0..2) == 0 {
                    // double bridge
                    let mut is: Vec<_> = (0..4).map(|_| rng.gen_range(0..n)).collect();
                    is.sort();
                    if is[0] == is[1] || is[1] == is[2] || is[2] == is[3] {
                        continue;
                    }
                    ps = ps[0..is[0] + 1]
                        .iter()
                        .chain(ps[is[2] + 1..is[3] + 1].iter())
                        .chain(ps[is[1] + 1..is[2] + 1].iter())
                        .chain(ps[is[0] + 1..is[1] + 1].iter())
                        .chain(ps[is[3] + 1..].iter())
                        .cloned()
                        .collect();
                } else {
                    for _ in 0..6 {
                        loop {
                            let i = rng.gen_range(1..n);
                            let j = rng.gen_range(1..n);
                            if i < j && j - i < n - 2 {
                                ps = ps[0..i]
                                    .iter()
                                    .chain(ps[i..j + 1].iter().rev())
                                    .chain(ps[j + 1..].iter())
                                    .cloned()
                                    .collect();
                                break;
                            }
                        }
                    }
                }
                break;
            }
        }
        min_ps
    }
}

const PRE: &'static str = "9 19 29 4 5 6 7 8 39 49 48 38 28 18 17 27 37 47 26 16 15 14 24 25 36 46 35 34 45 56 57 67 66 55 44 54 65 64 53 43 33 32 31 30 20 21 22 23 63 13 12 11 10 0 1 2 3 42 41 40 50 51 52 62 61 60 70 71 72 73 81 80 90 91 82 92 93 83 74 84 94 95 85 75 76 86 96 97 87 77 88 98 99 89 78 79 69 68 58 59
26 16 15 14 4 5 6 7 8 9 19 18 28 29 39 38 36 37 27 17 47 48 49 59 58 57 46 56 66 67 68 69 79 78 89 99 76 77 75 65 86 97 87 88 98 96 95 94 85 84 90 91 92 93 83 80 81 82 61 60 70 71 72 62 52 22 32 42 43 74 73 63 53 64 54 55 45 44 33 34 35 25 24 23 13 3 12 2 1 11 0 10 20 21 31 30 41 51 50 40
179 178 193 194 209 224 223 208 207 222 221 206 191 192 177 176 175 190 205 220 219 204 189 174 173 188 203 218 217 202 187 172 171 186 201 216 200 185 170 157 156 155 154 169 184 199 215 214 213 212 211 210 198 183 182 197 196 195 180 181 167 168 153 152 166 165 135 150 151 136 137 138 123 122 121 106 107 108 92 91 120 105 90 75 76 93 77 60 61 62 47 46 45 30 31 32 78 139 140 141 142 127 126 125 124 109 110 111 112 94 79 95 96 97 80 63 64 65 81 82 67 66 48 49 50 51 52 33 34 35 36 37 22 21 20 5 6 7 4 19 18 3 2 17 16 15 0 1 8 9 10 11 12 13 23 24 25 26 27 28 43 42 41 40 39 38 58 57 56 55 54 53 68 69 70 71 72 73 87 86 85 84 83 88 74 59 44 29 14 89 99 98 113 114 128 143 158 159 144 129 100 115 130 145 160 161 146 131 116 101 104 162 147 132 117 102 103 118 119 134 133 148 149 164 163
133 134 135 151 150 149 148 132 131 147 167 166 165 164 163 130 146 162 183 182 181 180 179 178 161 145 129 144 160 176 177 199 198 197 196 195 194 193 192 128 208 209 210 211 212 213 214 215 224 225 226 227 240 241 242 243 228 229 244 245 230 231 246 112 96 80 64 48 113 97 81 65 49 32 16 0 1 17 33 114 98 82 66 50 34 18 2 115 99 83 67 51 35 19 3 247 116 100 84 68 52 36 20 4 117 101 85 69 53 37 21 5 70 86 102 118 119 103 87 71 54 38 22 6 55 39 23 7 8 9 10 11 12 24 25 26 27 28 13 14 15 31 30 29 40 41 42 43 44 45 46 47 56 57 58 59 60 61 62 63 248 72 73 74 75 76 77 78 79 88 89 90 91 92 93 94 95 107 106 105 104 120 121 122 123 108 109 110 111 124 125 126 127 232 249 250 251 252 233 234 235 236 253 254 255 239 238 237 216 217 218 219 220 221 222 223 143 207 206 205 204 203 202 201 200 190 191 175 159 142 158 174 189 188 187 186 185 184 173 157 141 172 171 170 169 168 156 140 139 155 154 153 152 136 137 138
341 360 359 340 358 357 356 336 337 338 339 322 303 265 284 302 321 320 318 355 316 317 319 301 283 300 299 335 354 353 334 352 333 351 350 312 331 281 282 280 315 332 349 348 343 344 345 326 346 347 313 314 330 329 328 327 291 310 309 311 294 275 295 276 279 298 296 297 278 277 293 308 290 292 274 263 262 261 242 264 260 259 271 289 307 342 323 324 325 270 288 272 273 258 241 243 244 245 240 269 306 305 304 285 286 287 253 257 239 224 246 227 226 225 238 254 252 266 267 268 250 251 234 255 256 221 208 223 222 220 235 233 232 249 248 247 231 219 237 236 218 199 202 206 207 205 204 203 201 200 217 216 214 229 228 230 213 194 195 215 197 198 182 183 184 185 187 188 186 167 166 165 164 181 196 209 189 170 169 168 163 162 180 179 161 146 128 147 150 151 149 148 127 160 142 143 144 145 129 130 131 132 113 112 111 126 178 177 211 210 141 124 125 110 94 93 74 75 56 37 18 17 36 55 92 109 16 35 54 73 91 107 159 140 122 105 106 108 90 72 53 34 15 71 89 88 103 121 158 192 191 123 104 87 52 33 70 69 51 32 14 13 12 31 50 68 86 193 212 190 172 173 157 102 85 49 11 30 67 139 174 175 176 156 171 154 155 138 83 84 66 48 29 10 9 28 47 120 137 152 153 136 119 101 65 8 27 46 82 100 118 117 133 134 135 64 45 26 63 81 99 98 116 115 114 96 97 80 62 44 7 6 25 24 43 61 79 95 42 23 5 4 3 22 41 60 78 76 77 59 40 21 2 1 0 20 39 58 57 38 19
119 118 117 137 138 139 159 158 157 97 99 98 179 178 177 77 78 79 59 39 38 58 57 198 199 219 239 259 258 238 218 197 37 217 237 257 256 255 235 236 216 196 215 234 254 253 233 214 194 195 176 175 174 193 213 192 172 173 154 155 156 36 136 135 134 153 152 212 115 116 56 76 96 133 114 95 75 55 35 94 113 132 74 54 34 15 14 93 112 73 53 33 13 16 17 18 19 92 72 52 32 12 232 131 111 91 110 90 71 51 31 11 70 130 151 252 272 271 251 231 150 50 30 10 171 191 211 250 270 269 249 230 210 190 170 49 29 9 8 28 48 69 68 89 169 189 229 209 149 129 109 88 7 27 47 67 108 128 148 168 188 87 107 6 26 46 66 86 127 147 167 208 187 166 146 126 106 5 25 45 65 85 105 186 228 207 125 104 84 64 44 24 4 3 23 43 124 145 144 164 165 206 227 248 63 22 2 1 21 41 42 62 61 0 20 40 60 82 83 226 268 247 81 80 100 101 102 103 123 122 121 120 140 141 142 143 163 162 161 160 246 267 322 302 301 321 320 300 280 281 282 262 261 260 180 200 220 240 241 266 242 221 201 181 222 202 182 183 203 223 243 245 265 287 286 285 264 244 225 224 204 205 185 184 284 288 308 307 306 305 304 263 283 303 323 324 325 326 327 328 347 346 345 365 366 367 387 386 385 384 364 344 348 368 388 383 363 343 342 362 382 381 361 341 340 360 380 389 369 349 329 309 289 290 310 330 350 370 371 351 331 311 291 292 312 332 352 372 390 391 392 393 394 395 396 373 353 374 354 334 333 313 293 294 314 335 355 375 376 397 377 356 336 315 295 316 357 378 398 399 379 358 337 296 317 338 359 339 319 318 297 298 299 279 278 277 276 275 274 273
20 0 1 21 41 40 60 61 62 42 22 2 3 23 43 63 83 82 81 80 100 101 121 120 122 102 103 104 84 64 44 24 4 5 25 45 65 85 105 124 123 143 142 141 140 160 161 162 182 181 180 200 201 221 220 240 260 261 241 242 222 202 203 183 163 164 144 125 6 26 46 66 86 106 126 145 165 185 184 204 223 243 262 281 280 300 320 340 360 380 381 361 341 321 301 282 283 263 264 244 224 205 146 7 27 47 67 87 107 127 147 166 186 206 225 245 265 285 284 303 302 322 342 362 382 383 363 343 323 304 305 325 324 344 364 384 385 365 345 346 326 306 286 266 246 226 207 187 167 8 28 48 68 88 108 128 148 168 227 247 267 287 307 327 347 367 366 386 387 388 389 369 368 348 349 329 328 308 288 268 248 228 208 188 9 29 49 69 89 109 129 149 169 189 209 229 249 269 289 309 310 330 350 370 390 391 371 351 331 311 291 290 270 250 230 210 190 170 150 130 110 90 70 50 10 30 251 271 272 292 312 332 352 372 392 393 373 394 374 354 353 333 313 293 273 252 231 211 191 171 151 131 111 91 71 51 31 11 212 232 253 274 294 314 334 355 375 395 396 376 356 357 377 397 398 399 379 378 358 359 339 338 337 336 335 315 295 275 254 233 192 172 152 132 112 92 72 52 32 12 213 234 255 256 276 296 316 317 318 319 299 298 297 277 257 258 278 279 259 239 238 237 236 235 214 193 173 153 133 113 93 73 53 33 13 154 174 194 195 215 216 196 197 217 218 219 198 199 179 178 177 176 175 155 135 134 114 94 74 54 34 14 15 35 55 75 95 115 136 156 157 158 159 139 138 137 117 116 96 76 56 36 16 17 37 57 77 97 98 118 119 99 79 78 58 59 39 38 18 19
56 57 77 76 96 58 78 98 97 116 117 118 138 18 38 39 19 59 79 99 119 139 158 159 239 219 199 179 238 218 198 178 157 177 137 136 135 156 195 196 176 197 217 237 216 236 235 278 258 257 277 297 256 276 255 275 254 253 233 234 273 274 175 55 54 74 75 115 95 114 94 73 93 92 113 112 132 133 174 155 154 134 153 152 150 151 171 173 193 194 214 215 213 172 192 212 232 252 250 251 312 292 272 271 349 350 330 310 309 289 290 291 270 248 268 269 311 331 332 368 388 389 390 370 369 371 391 392 351 352 249 353 315 314 294 293 313 333 394 393 372 373 374 375 395 354 334 335 208 228 229 355 336 356 376 396 397 398 399 377 378 357 337 358 338 379 359 339 319 318 317 316 296 295 298 299 279 259 230 241 240 260 261 281 280 300 301 320 340 341 361 381 380 360 362 342 343 282 303 302 321 322 323 231 325 324 344 345 304 305 284 283 264 307 306 285 286 247 267 287 288 266 211 265 308 347 348 328 329 327 326 346 365 366 367 387 386 385 384 364 363 383 382 245 225 210 209 246 244 224 243 263 262 242 227 226 168 188 189 191 190 187 186 207 206 205 204 203 223 222 202 221 201 200 220 180 170 169 166 167 147 148 149 130 129 89 109 131 111 110 90 91 128 127 108 120 140 160 181 161 141 162 182 183 163 143 142 122 164 184 144 107 146 145 165 185 125 105 106 126 104 84 85 86 65 45 44 64 43 24 23 22 124 123 103 102 83 82 62 63 42 87 0 20 40 41 61 81 80 60 100 101 121 21 1 2 88 66 46 47 26 27 8 7 6 25 5 4 3 67 68 48 69 49 28 29 30 50 51 9 10 11 31 12 32 52 72 71 70 53 33 13 14 34 36 35 15 16 17 37
329 309 310 330 349 369 389 390 370 350 311 331 351 371 391 392 372 352 332 312 353 373 393 394 374 333 354 375 395 396 376 355 313 334 356 377 397 398 399 379 378 357 335 336 337 358 359 338 339 319 318 317 316 314 315 298 299 279 278 297 296 277 258 259 239 238 257 295 276 237 218 219 199 179 159 158 178 198 217 256 275 294 236 197 177 157 216 196 176 156 155 175 195 255 235 215 274 254 234 214 139 119 99 79 59 39 19 18 38 58 78 98 118 138 17 37 57 77 97 117 137 293 273 253 233 213 16 36 56 76 96 116 136 75 55 35 15 14 34 54 74 95 115 135 292 272 252 232 94 53 33 13 12 32 73 93 114 212 52 31 11 10 30 50 51 72 134 113 92 71 70 291 271 251 231 91 90 112 133 154 211 192 193 194 174 173 153 132 111 110 152 172 191 290 270 250 230 210 171 151 131 130 150 170 190 289 269 249 229 209 189 169 149 129 268 288 248 228 208 188 168 148 128 308 328 348 368 388 387 367 347 327 307 287 267 247 227 207 187 167 147 127 386 366 346 326 306 286 266 246 385 365 345 325 305 285 265 226 206 186 166 146 126 245 384 364 344 324 304 284 264 244 383 363 343 323 303 283 263 243 382 362 342 225 205 185 165 145 125 322 302 282 262 242 341 361 381 380 360 340 321 301 281 261 241 320 300 280 260 240 224 204 184 164 144 124 223 203 183 163 202 222 221 220 200 201 182 162 143 123 142 161 181 180 160 140 141 122 121 120 100 101 102 103 104 82 81 80 60 61 62 83 84 63 40 41 42 21 20 0 1 2 22 43 64 105 85 65 44 23 3 4 24 45 106 86 66 25 5 6 26 46 107 87 67 47 27 7 68 88 108 109 89 69 48 28 8 9 29 49
602 601 600 575 576 577 603 578 550 551 552 553 528 529 554 579 604 530 555 527 525 526 580 605 606 607 608 609 582 581 556 557 558 583 584 585 610 611 586 533 532 531 500 501 507 508 534 559 561 587 612 560 506 483 509 535 562 536 505 502 475 476 503 504 484 537 613 588 563 510 481 482 477 478 479 480 511 538 614 589 564 512 487 457 456 450 451 425 452 453 454 455 431 432 458 459 485 486 513 590 615 616 591 539 565 566 592 617 618 567 540 433 426 427 428 429 430 434 460 514 541 542 568 593 619 620 595 594 543 488 461 515 516 517 569 570 571 596 621 622 623 597 624 599 598 572 544 489 435 409 404 403 402 401 405 408 436 462 490 518 545 573 574 549 548 547 546 519 491 464 463 437 410 407 406 400 377 378 379 411 493 520 521 522 523 524 494 492 465 438 412 383 380 382 381 376 375 352 385 384 439 466 467 468 469 495 496 497 498 499 440 387 386 357 354 353 351 350 355 356 358 359 413 414 441 442 470 472 473 474 471 443 415 445 444 417 416 389 388 362 361 360 334 333 332 331 330 329 328 326 325 327 307 308 390 418 446 448 449 447 419 392 391 363 337 336 335 309 306 305 304 303 302 301 300 311 364 393 420 421 422 423 424 394 365 366 367 368 395 396 369 312 310 278 277 276 275 279 280 281 338 370 397 398 399 371 343 342 341 340 339 252 251 250 253 254 255 282 313 344 345 372 373 374 346 257 228 225 226 227 229 256 283 314 315 316 317 319 347 348 349 320 318 285 284 258 230 202 200 201 203 231 290 293 294 321 322 323 324 295 289 288 259 204 205 232 286 287 291 292 260 234 233 206 178 175 176 177 179 180 181 261 262 296 297 298 299 264 263 235 155 150 151 152 154 156 153 125 126 127 128 207 208 236 237 129 100 101 103 130 105 106 102 75 76 104 131 182 183 209 210 238 265 266 267 271 272 273 274 212 211 184 77 51 50 25 26 52 27 0 1 2 3 28 53 78 79 157 185 186 239 240 241 268 270 242 213 132 54 29 158 159 187 214 243 269 249 248 247 215 160 133 80 55 30 4 107 134 188 189 216 244 245 246 217 135 108 82 81 56 31 5 6 7 32 57 83 109 161 162 190 224 223 222 221 220 219 218 191 163 110 84 58 8 33 136 137 192 193 194 196 85 59 34 9 111 164 165 195 197 198 199 166 138 112 86 60 35 10 139 167 168 141 140 113 114 87 61 36 11 12 37 62 88 89 115 142 170 172 173 174 171 169 143 116 63 38 13 90 117 144 145 146 147 148 149 118 92 91 64 39 14 65 93 119 120 121 122 123 124 94 66 40 15 41 16 17 42 67 99 98 97 96 95 68 43 18 19 44 69 70 45 20 71 72 73 48 47 46 21 22 23 24 49 74
702 675 676 703 704 677 648 649 650 622 621 594 595 623 705 678 651 596 568 567 540 541 569 624 706 679 652 597 542 514 513 486 487 488 515 570 625 707 680 653 598 571 543 516 489 544 626 599 654 681 708 709 710 683 682 655 627 572 545 517 518 600 656 628 573 546 519 492 491 493 494 521 520 547 548 574 601 629 575 490 54 27 0 1 28 55 81 108 82 2 29 56 83 109 135 162 189 216 217 190 163 136 110 3 30 57 84 137 164 191 218 602 138 111 4 31 58 85 112 139 165 192 219 166 5 32 59 86 113 140 167 193 194 60 33 6 7 8 35 34 61 87 114 141 168 195 221 220 222 223 224 197 196 169 62 88 142 170 463 462 461 460 459 432 433 434 405 406 407 435 115 89 143 351 378 379 408 436 380 352 324 297 270 243 271 298 325 353 381 464 409 247 244 326 299 272 245 246 354 437 382 327 300 273 274 301 328 355 410 603 465 438 383 248 116 275 302 329 356 411 466 439 384 357 330 303 276 249 412 467 440 413 386 385 358 331 304 277 250 251 278 305 332 359 576 604 630 657 684 711 712 685 658 631 577 549 522 495 550 713 686 659 632 605 578 523 496 551 714 687 660 633 606 579 524 497 552 661 688 715 716 689 662 634 607 580 525 498 553 635 717 690 663 608 581 526 554 636 691 718 719 692 665 664 609 582 555 527 360 499 500 501 528 637 583 556 529 502 503 530 557 610 638 584 387 414 441 468 469 442 361 333 388 415 443 470 471 472 444 416 389 362 334 306 279 252 307 280 253 117 445 417 390 363 335 308 281 254 611 473 446 418 391 364 336 309 282 255 337 419 447 474 475 476 449 448 420 392 365 310 283 311 338 393 421 422 366 339 312 284 257 144 90 118 256 258 285 394 340 313 286 259 260 287 314 367 395 341 171 145 91 63 36 9 10 37 64 119 172 198 225 226 199 146 92 65 38 11 173 200 227 229 228 201 174 147 120 93 66 39 12 202 368 230 175 148 121 94 67 40 13 176 203 612 231 204 149 122 95 68 41 14 177 205 232 233 206 178 150 96 69 42 15 123 179 151 97 70 43 16 17 44 71 98 124 152 639 585 613 666 693 720 721 694 667 640 586 558 722 695 668 641 614 559 531 504 505 532 587 723 696 669 642 615 560 533 506 125 724 697 670 643 588 561 534 507 616 644 671 698 725 726 699 672 589 562 369 535 617 645 673 700 727 728 701 674 647 646 618 590 563 536 508 509 591 619 620 593 592 564 537 510 511 538 565 566 539 512 396 342 370 397 423 424 451 450 477 478 479 481 480 452 425 398 343 371 453 454 426 315 316 344 399 427 482 455 400 372 288 261 262 289 317 345 373 428 456 483 484 485 458 457 429 401 318 290 263 126 346 374 402 430 431 404 403 375 347 319 291 264 320 348 349 376 377 350 323 322 321 292 293 294 295 296 269 268 267 266 265 153 127 99 72 45 18 19 46 73 100 154 180 207 234 235 208 181 128 101 74 47 20 155 182 209 236 238 237 210 211 183 156 129 102 75 48 21 184 239 212 157 130 103 76 49 22 158 185 213 240 241 214 186 131 104 77 50 23 159 187 242 215 188 161 160 132 105 78 51 24 106 133 134 107 80 79 52 25 26 53
277 307 306 276 275 305 304 274 273 303 302 301 300 270 271 272 243 244 242 241 240 210 211 212 213 214 245 246 247 217 216 215 184 183 182 181 180 150 151 152 120 121 122 153 185 186 154 123 92 91 90 60 30 31 61 62 32 93 124 155 187 156 125 94 63 33 64 34 35 65 95 126 157 96 66 36 6 5 4 3 2 1 0 127 97 67 128 158 98 68 38 37 7 8 9 39 69 99 129 159 188 189 190 160 130 100 70 40 10 11 41 71 101 131 161 191 12 42 72 102 132 162 192 103 73 43 13 14 44 74 104 134 133 163 193 164 29 28 27 26 25 55 56 57 58 59 89 88 87 86 85 115 116 117 118 119 149 148 147 146 145 175 176 177 178 179 205 206 207 208 209 194 235 236 237 238 239 269 268 267 266 265 298 299 329 359 358 328 297 296 295 327 357 388 389 419 449 448 418 387 326 356 386 417 447 446 416 385 355 325 415 445 444 414 384 354 195 204 174 144 114 84 54 24 23 53 83 113 143 173 203 22 52 82 112 142 172 202 324 165 111 81 51 21 20 50 80 110 141 171 201 196 166 135 136 140 109 79 49 19 18 48 78 108 105 106 107 137 139 170 138 167 77 17 47 76 75 45 15 16 46 197 200 169 168 294 474 475 476 477 478 479 509 508 507 506 505 504 534 535 536 537 538 539 569 568 567 566 564 565 597 598 599 629 628 627 596 594 595 657 658 659 689 719 718 688 687 717 199 198 264 624 625 626 747 748 749 779 778 777 776 746 716 686 656 655 654 685 715 745 775 805 835 834 804 774 744 684 714 743 773 803 833 828 829 830 831 832 802 772 742 713 683 653 234 712 741 771 801 800 770 799 798 768 769 740 711 682 652 681 710 739 738 708 709 680 651 623 622 650 679 678 648 649 229 228 233 621 620 619 618 593 592 591 590 589 588 558 559 560 561 562 563 232 230 231 263 262 533 532 531 530 529 528 259 260 261 293 292 291 503 502 501 500 499 498 258 227 289 290 321 323 322 473 472 471 470 469 320 353 352 351 319 288 257 468 440 441 442 383 382 350 381 411 412 413 443 439 410 380 349 318 287 226 256 317 348 379 409 438 408 378 377 347 316 286 255 225 224 223 222 254 285 346 407 376 315 284 253 252 251 221 220 250 249 219 218 248 283 314 345 437 406 375 374 344 343 313 312 282 281 311 342 373 405 436 404 403 372 341 310 280 279 278 308 309 340 371 402 435 467 466 434 433 432 401 370 339 431 465 464 463 462 461 400 369 338 368 491 497 496 495 494 493 492 430 399 429 459 460 490 489 488 458 428 427 457 487 486 456 426 398 527 526 525 524 523 522 521 551 552 553 554 555 556 557 587 586 585 584 583 613 614 615 616 645 644 643 642 612 582 581 611 641 646 617 397 396 366 367 337 336 335 365 395 364 334 333 332 362 363 394 393 392 361 331 330 360 390 391 422 423 424 425 421 420 450 451 452 453 454 455 485 484 483 482 481 480 640 647 639 638 608 609 610 580 579 578 548 549 550 520 519 518 517 547 516 546 515 545 575 576 577 607 637 636 606 605 635 634 604 510 511 512 513 514 544 574 633 603 573 543 542 541 540 570 571 572 602 632 631 601 600 630 660 690 720 750 661 691 721 751 780 810 840 870 871 841 811 781 662 692 722 752 782 812 842 872 873 843 813 783 753 723 693 663 677 874 844 814 784 754 724 694 664 665 695 725 755 785 815 845 875 756 726 696 666 667 697 727 757 786 816 846 876 787 817 847 877 878 848 818 707 676 668 698 728 758 788 879 849 819 789 759 729 699 669 670 675 706 700 730 760 790 820 850 880 701 671 672 673 674 705 737 736 704 703 702 731 761 791 821 851 881 732 735 734 733 762 767 766 765 764 763 792 822 852 882 793 797 796 795 794 823 853 883 824 825 826 827 855 854 884 885 886 856 857 887 888 858 859 889 890 860 861 891 892 862 863 893 894 864 865 895 866 896 897 867 868 898 899 869 839 809 808 838 837 807 806 836
60 30 0 1 31 61 62 32 2 3 33 63 64 34 4 5 35 65 66 36 6 7 37 67 68 38 8 9 39 69 70 40 10 11 41 71 72 42 12 13 43 73 74 44 14 15 45 75 76 46 16 17 47 77 78 48 18 19 49 79 80 50 20 21 51 81 82 52 22 23 53 83 84 54 24 25 55 85 86 56 26 27 57 87 88 58 28 29 59 89 119 118 117 147 148 149 179 178 177 207 208 209 239 238 237 267 268 269 299 298 297 327 328 329 359 358 357 387 388 389 419 418 417 447 448 449 479 478 477 507 508 509 539 538 537 567 568 569 599 598 597 627 628 629 659 658 657 687 688 689 719 718 717 747 748 749 779 778 777 807 808 809 839 869 899 898 868 838 837 867 897 896 866 836 835 865 895 894 864 834 833 863 893 892 862 832 831 861 891 890 860 830 829 859 889 888 858 828 827 857 887 886 856 826 825 855 885 884 854 824 823 853 883 882 852 822 821 851 881 880 850 820 819 849 879 878 848 818 817 847 877 876 846 816 815 845 875 874 844 814 813 843 873 872 842 812 811 841 871 870 840 810 780 781 782 752 751 750 720 721 722 692 691 690 660 661 662 632 631 630 600 601 602 572 571 570 540 541 542 512 511 510 480 481 482 452 451 450 420 421 422 392 391 390 360 361 362 332 331 330 300 301 302 272 271 270 240 241 242 212 211 210 180 181 182 150 120 90 91 121 151 152 122 92 93 123 153 154 124 94 95 125 155 156 126 96 97 127 157 158 128 98 99 129 159 160 130 100 101 131 161 162 132 102 103 133 163 164 134 104 105 135 165 166 136 106 107 137 167 168 138 108 109 139 169 170 140 110 111 141 171 172 142 112 113 143 173 144 114 115 116 146 145 174 175 176 206 205 204 234 235 236 266 265 264 294 295 296 326 325 324 354 355 356 386 385 384 414 415 416 446 445 444 474 475 476 506 505 504 534 535 536 566 565 564 594 595 596 626 625 624 654 655 656 686 685 684 714 715 716 746 745 744 774 775 776 806 805 804 803 773 743 742 772 802 801 771 741 740 770 800 799 769 739 738 768 798 797 767 737 736 766 796 795 765 735 734 764 794 793 763 733 732 762 792 791 761 731 730 760 790 789 759 729 728 758 788 787 757 727 726 756 786 785 755 725 754 784 783 753 723 724 695 694 693 663 664 665 635 634 633 603 604 605 575 574 573 543 544 545 515 514 513 483 484 485 455 454 453 423 424 425 395 394 393 363 364 365 335 334 333 303 304 305 275 274 273 243 213 183 184 214 244 245 215 185 186 216 246 247 217 187 188 218 248 249 219 189 190 220 250 251 221 191 192 222 252 253 223 193 194 224 254 255 225 195 196 226 256 257 227 197 258 228 198 199 229 259 260 230 200 201 231 261 262 232 202 203 233 263 293 292 291 321 322 323 353 352 351 381 382 383 413 412 411 441 442 443 473 472 471 501 502 503 533 532 531 561 562 563 593 592 591 621 622 623 653 652 651 681 682 683 713 712 711 710 680 650 649 679 709 708 678 648 647 677 707 706 676 646 645 675 705 704 674 644 643 673 703 702 672 642 641 671 701 700 670 640 639 669 699 698 697 696 666 667 668 638 637 636 606 607 608 576 577 578 548 547 546 516 517 518 488 487 486 456 457 458 428 427 426 396 397 398 368 367 366 336 337 338 308 307 306 276 277 278 339 309 279 280 310 340 341 311 281 282 312 342 343 313 283 284 314 344 345 315 285 286 316 346 347 317 287 288 289 290 320 319 318 348 349 350 380 379 378 408 409 410 440 439 438 468 469 470 500 499 498 528 529 530 560 559 558 588 589 590 620 619 618 617 587 557 556 586 616 615 585 555 554 584 614 613 583 553 552 582 612 611 581 551 580 610 609 579 549 550 521 520 519 489 490 491 461 460 459 429 430 400 399 369 370 431 401 371 372 402 432 433 403 373 374 404 434 435 405 375 376 377 407 406 436 437 467 466 465 495 496 497 527 526 525 524 494 464 463 493 523 522 492 462
788 789 819 818 848 849 879 878 877 876 846 847 817 787 786 816 815 814 813 843 844 845 875 874 873 872 871 870 840 841 842 812 811 810 780 781 782 783 784 785 755 756 757 727 726 725 724 754 753 752 722 723 693 663 633 603 602 632 662 692 691 721 751 750 720 690 660 661 631 630 600 601 571 570 540 541 511 510 480 481 451 450 420 390 391 421 361 360 330 331 301 300 270 271 241 240 210 180 150 120 90 60 30 0 1 2 3 33 32 31 61 91 121 122 123 153 152 151 181 182 183 213 243 273 272 242 212 211 422 452 423 453 455 456 457 427 426 425 395 365 335 336 337 307 306 305 304 334 364 363 333 303 302 332 362 392 393 394 424 454 484 485 486 487 517 516 515 514 513 483 482 512 542 572 573 543 544 545 575 574 604 605 635 634 664 694 695 665 666 696 697 667 668 698 728 758 759 729 699 700 701 671 670 669 639 638 637 636 606 607 608 609 610 640 641 611 581 580 550 520 490 491 521 551 552 522 492 493 494 495 525 524 523 553 554 555 556 557 587 586 585 584 583 613 614 615 616 617 647 646 645 644 643 642 612 582 579 578 577 576 546 547 548 549 519 518 488 489 459 458 428 398 397 396 366 367 368 369 370 340 310 311 312 313 343 373 403 402 372 342 341 371 401 400 399 429 460 430 339 309 338 308 278 279 249 248 247 277 276 275 274 244 245 246 216 186 187 217 218 188 158 128 129 159 189 219 190 220 250 280 281 251 221 191 192 162 222 223 193 163 164 165 135 136 166 167 137 107 108 109 79 78 77 47 17 16 46 76 106 105 75 45 15 14 44 74 104 134 133 132 102 103 73 72 71 101 131 161 160 130 100 70 69 99 98 68 38 39 40 41 42 43 13 12 11 10 9 8 7 37 67 97 96 66 36 6 5 4 34 64 63 62 92 93 94 124 154 184 214 215 185 155 156 157 127 126 125 95 65 35 431 461 432 462 463 433 229 228 227 226 225 224 194 195 196 197 198 199 200 201 231 230 260 261 262 263 264 265 266 267 297 296 295 294 293 323 353 352 322 292 291 290 289 259 258 257 256 255 254 253 252 282 283 284 285 286 287 288 318 319 320 321 351 381 411 410 380 350 349 379 409 408 407 406 376 377 378 348 347 317 316 346 345 315 314 344 374 375 405 404 434 464 465 435 436 466 496 526 527 497 467 437 438 468 469 439 440 470 500 499 498 528 529 530 531 501 471 441 442 472 473 443 474 475 445 444 414 413 412 382 383 384 354 324 325 355 385 415 416 446 476 477 447 417 387 357 327 326 356 386 388 358 418 419 389 359 329 328 298 299 269 268 238 239 209 208 178 179 149 148 147 177 176 146 85 84 54 53 52 22 23 24 25 55 56 26 27 28 29 59 58 57 87 88 89 119 118 117 116 86 115 114 144 145 175 205 206 207 237 236 235 234 233 232 202 203 204 174 173 143 113 83 82 81 51 21 20 19 18 48 49 50 80 110 140 139 138 168 169 170 171 141 111 112 142 172 448 449 479 478 508 509 539 538 564 563 533 503 502 532 562 561 560 559 558 588 618 648 649 619 589 590 591 592 593 594 595 565 568 569 599 629 659 658 628 598 597 567 537 507 506 505 504 534 535 536 566 596 626 627 657 656 655 625 624 654 684 685 715 714 744 745 746 747 748 718 717 716 686 687 688 689 719 749 779 778 777 776 775 805 806 807 808 809 839 869 899 898 868 838 837 867 897 896 866 836 835 865 895 894 864 834 804 774 773 803 833 863 893 892 862 832 802 772 742 743 713 683 653 623 622 652 682 712 711 741 771 770 740 710 680 681 651 621 620 650 679 709 708 678 677 707 676 675 674 673 672 702 732 731 730 760 761 762 763 733 703 704 705 706 736 735 734 764 765 766 767 737 738 739 769 768 798 799 800 801 831 861 891 890 860 830 829 828 858 859 889 888 887 886 885 884 854 855 856 857 827 797 796 826 825 795 794 824 823 793 792 822 821 791 790 820 850 880 881 882 883 853 852 851
23 24 25 28 27 26 61 62 60 129 130 95 96 97 132 131 94 93 59 58 21 22 57 92 91 127 126 128 56 18 19 20 54 55 90 89 88 87 122 53 52 17 51 50 15 16 86 189 224 225 191 190 154 155 121 156 120 85 117 82 83 47 48 49 14 13 84 119 118 153 152 151 116 45 46 81 80 113 114 79 44 9 10 11 12 115 150 188 187 186 185 184 149 148 147 146 38 39 40 74 109 144 110 75 111 112 78 77 4 5 6 7 42 43 8 41 76 182 183 221 222 220 219 256 255 254 253 218 290 291 326 325 329 364 328 363 293 292 327 362 397 398 399 257 223 258 259 260 261 226 294 295 296 297 262 263 227 192 157 193 228 264 229 230 195 194 125 124 159 158 123 160 164 163 198 162 197 161 196 231 265 266 301 267 302 268 303 304 232 233 234 269 270 271 272 298 299 300 437 402 401 400 366 365 330 331 332 367 368 333 334 335 370 336 337 371 406 369 404 405 403 439 438 473 472 576 575 540 541 542 507 508 543 509 510 506 504 505 469 470 501 466 431 285 286 287 288 323 324 289 322 319 320 321 356 355 357 358 359 361 360 396 395 394 393 429 428 430 465 500 612 647 611 681 646 680 645 610 644 609 608 607 642 640 641 606 571 605 570 535 536 573 572 574 539 538 537 502 503 468 467 432 433 434 435 436 471 441 442 407 372 443 444 408 409 374 373 338 339 341 340 305 479 587 586 621 656 655 620 585 550 549 584 619 654 652 653 551 517 516 515 514 477 478 513 548 547 512 440 474 475 476 511 546 480 445 446 481 482 199 200 235 165 166 167 201 236 237 98 99 173 138 137 103 102 67 32 34 33 68 69 104 139 174 209 208 101 31 66 65 30 64 29 63 100 134 135 136 171 170 279 314 349 348 313 276 277 278 244 243 242 172 207 206 205 240 241 275 310 345 311 312 204 169 168 133 203 202 238 239 274 273 308 309 344 343 447 412 411 376 375 410 377 342 307 306 448 413 378 379 414 416 415 380 450 485 449 484 483 518 553 552 519 554 588 624 589 659 694 695 697 696 732 733 731 729 730 764 765 800 766 660 661 626 625 590 591 520 555 556 521 486 557 522 487 451 452 453 454 489 488 523 524 558 559 593 628 592 627 662 663 664 699 698 629 594 418 419 384 383 417 382 347 381 346 581 583 582 617 618 616 651 615 544 545 580 579 614 577 578 613 648 649 786 750 751 752 716 715 717 682 683 684 685 650 686 687 861 826 825 827 622 657 623 658 693 692 728 727 691 726 689 690 725 724 795 760 761 759 794 758 793 792 790 791 894 860 859 824 789 754 755 756 757 688 723 722 828 829 864 899 830 865 903 868 801 836 837 835 869 834 833 799 798 797 796 763 762 832 867 866 831 936 901 900 935 902 937 904 939 938 973 974 972 971 1006 1041 970 1005 1004 934 969 1040 1075 1074 1039 1073 1038 1003 968 1106 1107 1072 1071 1036 1037 1001 1002 967 932 897 863 862 933 898 966 931 896 895 999 964 965 930 929 823 858 893 928 927 963 962 961 960 926 891 1000 1035 1034 1070 1069 1068 721 720 719 718 753 788 787 1224 1223 1222 1082 1117 1152 1187 1221 1186 1009 1044 1078 1079 1080 1045 1189 1188 1153 1118 1154 1119 1084 1049 1048 1083 1047 1046 1012 1011 1010 940 975 1014 979 944 909 839 874 767 802 768 803 804 769 734 838 873 872 908 907 977 1013 978 943 942 941 905 906 870 871 976 1081 1116 1151 1115 1150 1220 1219 1185 1184 1149 1114 1113 1148 1218 1183 1182 1147 1181 1146 1008 1043 1042 1007 1077 1112 1111 1076 1110 1145 1109 1108 1143 1178 1179 1144 1180 1215 1214 1216 1217 1213 1212 1142 1177 1211 1176 1141 1175 1210 1209 1174 1172 1173 1139 1138 1098 1168 1133 1132 1167 1202 1201 1203 1134 1169 1170 1205 1204 1135 1099 1100 1101 1136 1171 1206 1207 1208 1137 1103 1104 1105 1140 1102 1067 998 1033 1032 822 857 892 821 785 820 819 856 855 854 889 890 924 959 925 853 888 957 922 923 958 993 994 995 997 996 1031 1066 1065 1064 1063 1062 1097 1061 1060 1025 1026 990 991 992 1027 1028 1029 1030 887 852 816 817 784 818 783 679 714 713 748 749 747 712 782 745 780 781 851 850 886 1022 987 988 989 953 954 921 956 955 919 920 885 884 883 848 849 814 815 813 778 779 918 812 847 882 917 916 952 951 986 985 1020 950 984 949 948 913 914 915 880 881 983 982 1018 1019 1122 1087 1088 1195 1194 1193 1192 1157 1158 1123 1160 1159 1124 1089 1054 1053 1052 1017 1055 1090 1125 1091 1126 1092 1127 1196 1197 1162 1161 1093 1128 1163 1021 1056 1057 1058 1023 1024 1059 1094 1129 1164 1199 1198 1200 1165 1166 1131 1130 1095 1096 746 711 710 709 708 736 771 735 770 805 806 807 1085 1050 1190 1191 1155 1120 1121 1156 1086 1051 1015 1016 981 911 946 945 980 910 875 947 912 878 879 877 842 841 840 876 843 808 809 844 845 810 811 846 776 775 773 774 739 738 703 704 705 670 669 668 601 600 671 636 635 634 633 563 598 599 564 632 631 667 666 665 700 701 702 737 772 777 744 743 742 706 741 740 707 672 637 602 567 463 464 499 534 498 533 568 569 603 604 638 639 673 674 675 676 677 678 643 566 565 531 530 532 427 462 497 496 495 460 461 426 391 392 390 389 354 425 424 423 388 387 422 457 458 459 492 493 494 421 386 351 350 315 316 385 420 456 455 490 561 562 597 527 528 529 526 491 525 560 595 596 630 353 352 318 282 317 283 248 284 249 145 180 179 214 215 216 217 181 250 251 252 213 212 177 178 143 247 246 211 210 245 280 281 175 176 140 105 70 35 141 73 72 142 107 108 106 71 37 36 1 0 2 3
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 79 78 77 76 75 74 73 72 71 70 69 68 67 66 65 64 63 62 61 60 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 159 158 157 156 155 154 153 152 151 150 149 148 147 146 145 144 143 142 141 140 139 138 137 136 135 134 133 132 131 130 129 128 127 126 125 124 123 122 121 120 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 239 238 237 236 235 234 233 232 231 230 229 228 227 226 225 224 223 222 221 220 219 218 217 216 215 214 213 212 211 210 209 208 207 206 205 204 203 202 201 200 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 319 318 317 316 315 314 313 312 311 310 309 308 307 306 305 304 303 302 301 300 299 298 297 296 295 294 293 292 291 290 289 288 287 286 285 284 283 282 281 280 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 399 398 397 396 395 394 393 392 391 390 389 388 387 386 385 384 383 382 381 380 379 378 377 376 375 374 373 372 371 370 369 368 367 366 365 364 363 362 361 360 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 479 478 477 476 475 474 473 472 471 470 469 468 467 466 465 464 463 462 461 460 459 458 457 456 455 454 453 452 451 450 449 448 447 446 445 444 443 442 441 440 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 559 558 557 556 555 554 553 552 551 550 549 548 547 546 545 544 543 542 541 540 539 538 537 536 535 534 533 532 531 530 529 528 527 526 525 524 523 522 521 520 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 639 638 637 636 635 634 633 632 631 630 629 628 627 626 625 624 623 622 621 620 619 618 617 616 615 614 613 612 611 610 609 608 607 606 605 604 603 602 601 600 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 719 718 717 716 715 714 713 712 711 710 709 708 707 706 705 704 703 702 701 700 699 698 697 696 695 694 693 692 691 690 689 688 687 686 685 684 683 682 681 680 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 799 798 797 796 795 794 793 792 791 790 789 788 787 786 785 784 783 782 781 780 779 778 777 776 775 774 773 772 771 770 769 768 767 766 765 764 763 762 761 760 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 832 833 834 835 836 837 838 839 879 878 877 876 875 874 873 872 871 870 869 868 867 866 865 864 863 862 861 860 859 858 857 856 855 854 853 852 851 850 849 848 847 846 845 844 843 842 841 840 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 915 916 917 918 919 959 958 957 956 955 954 953 952 951 950 949 948 947 946 945 944 943 942 941 940 939 938 937 936 935 934 933 932 931 930 929 928 927 926 925 924 923 922 921 920 960 961 962 963 964 965 966 967 968 969 970 971 972 973 974 975 976 977 978 979 980 981 982 983 984 985 986 987 988 989 990 991 992 993 994 995 996 997 998 999 1039 1038 1037 1036 1035 1034 1033 1032 1031 1030 1029 1028 1027 1026 1025 1024 1023 1022 1021 1020 1019 1018 1017 1016 1015 1014 1013 1012 1011 1010 1009 1008 1007 1006 1005 1004 1003 1002 1001 1000 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 1079 1119 1118 1117 1116 1115 1114 1113 1112 1111 1110 1109 1108 1107 1106 1105 1104 1103 1102 1101 1100 1099 1098 1097 1096 1095 1094 1093 1092 1091 1090 1089 1088 1087 1086 1085 1084 1083 1082 1081 1080 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 1136 1137 1138 1139 1140 1141 1142 1143 1144 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1199 1198 1197 1196 1195 1194 1193 1192 1191 1190 1189 1188 1187 1186 1185 1184 1183 1182 1181 1180 1179 1178 1177 1176 1175 1174 1173 1172 1171 1170 1169 1168 1167 1166 1165 1164 1163 1162 1161 1160 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 1213 1214 1215 1216 1217 1218 1219 1220 1221 1222 1223 1224 1225 1226 1227 1228 1229 1230 1231 1232 1233 1234 1235 1236 1237 1238 1239 1279 1278 1277 1276 1275 1274 1273 1272 1271 1270 1269 1268 1267 1266 1265 1264 1263 1262 1261 1260 1259 1258 1257 1256 1255 1254 1253 1252 1251 1250 1249 1248 1247 1246 1245 1244 1243 1242 1241 1240 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1315 1316 1317 1318 1319 1359 1358 1357 1356 1355 1354 1353 1352 1351 1350 1349 1348 1347 1346 1345 1344 1343 1342 1341 1340 1339 1338 1337 1336 1335 1334 1333 1332 1331 1330 1329 1328 1327 1326 1325 1324 1323 1322 1321 1320 1360 1361 1362 1363 1364 1365 1366 1367 1368 1369 1370 1371 1372 1373 1374 1375 1376 1377 1378 1379 1380 1381 1382 1383 1384 1385 1386 1387 1388 1389 1390 1391 1392 1393 1394 1395 1396 1397 1398 1399 1439 1438 1437 1436 1435 1434 1433 1432 1431 1430 1429 1428 1427 1426 1425 1424 1423 1422 1421 1420 1419 1418 1417 1416 1415 1414 1413 1412 1411 1410 1409 1408 1407 1406 1405 1404 1403 1402 1401 1400 1440 1441 1442 1443 1444 1445 1446 1447 1448 1449 1450 1451 1452 1453 1454 1455 1456 1457 1458 1459 1460 1461 1462 1463 1464 1465 1466 1467 1468 1469 1470 1471 1472 1473 1474 1475 1476 1477 1478 1479 1519 1518 1517 1516 1515 1514 1513 1512 1511 1510 1509 1508 1507 1506 1505 1504 1503 1502 1501 1500 1499 1498 1497 1496 1495 1494 1493 1492 1491 1490 1489 1488 1487 1486 1485 1484 1483 1482 1481 1480 1520 1521 1522 1523 1524 1525 1526 1527 1528 1529 1530 1531 1532 1533 1534 1535 1536 1537 1538 1539 1540 1541 1542 1543 1544 1545 1546 1547 1548 1549 1550 1551 1552 1553 1554 1555 1556 1557 1558 1559 1599 1598 1597 1596 1595 1594 1593 1592 1591 1590 1589 1588 1587 1586 1585 1584 1583 1582 1581 1580 1579 1578 1577 1576 1575 1574 1573 1572 1571 1570 1569 1568 1567 1566 1565 1564 1563 1562 1561 1560
525 524 484 485 445 444 404 405 406 446 407 447 487 486 526 527 528 488 489 529 530 490 450 449 448 408 409 410 411 412 413 453 452 451 491 531 532 492 493 533 534 494 454 414 415 455 495 535 536 496 456 416 417 418 458 457 497 498 537 538 578 577 576 575 574 573 613 612 572 571 570 569 609 610 611 651 650 649 648 608 568 567 566 606 607 647 646 686 687 688 689 690 691 692 652 653 654 614 615 616 617 618 658 657 656 655 694 693 733 732 731 730 729 728 727 767 768 807 808 809 769 770 771 772 773 813 812 811 810 850 890 891 851 852 892 893 853 854 814 774 734 735 695 696 697 698 737 736 775 815 855 895 894 889 849 848 847 726 766 806 846 845 805 765 725 685 645 605 565 564 604 644 684 724 764 804 844 843 803 763 723 722 682 683 643 642 602 603 563 562 561 560 600 601 641 640 680 681 721 720 760 761 762 802 842 841 801 800 840 880 881 882 883 884 885 886 926 925 924 923 922 921 920 960 1000 1040 1080 1120 1160 1200 1240 1280 1320 1360 1400 1440 1480 1520 1560 1081 1041 1001 961 962 963 964 965 966 887 888 896 856 816 776 777 738 1006 1005 1004 1003 1002 1042 1043 1044 1084 1083 1082 1122 1123 1124 1125 1085 1045 1046 1086 1126 1166 1165 1164 1163 1203 1202 1162 1121 1161 1201 1241 1242 1243 1244 1204 1205 1206 1246 1245 1285 1286 1326 1325 1284 1283 1282 1281 1321 1322 1323 1324 1364 1404 1363 1362 1361 1401 1402 1403 1443 1444 1445 1405 1365 1366 1406 1446 1486 1485 1484 1524 1523 1483 1482 1442 1441 1481 1522 1521 1561 1562 1563 1564 1565 1525 1526 1566 1567 1527 1487 1488 1489 1529 1528 1568 1569 1570 1571 1531 1530 1490 1491 1451 1450 1449 1448 1447 1407 1408 1409 1410 1411 1371 1370 1369 1368 1367 1327 1287 1288 1328 1329 1289 1290 1330 1331 1291 1292 1332 1372 1412 1452 1492 1532 1572 1573 1533 1493 1453 1413 1373 1333 1293 1253 1252 1251 1250 1249 1248 1247 1207 1167 1127 1087 1047 1007 967 927 928 817 778 857 897 968 1008 1048 1088 1128 1168 1208 1209 1210 1211 1212 1213 1173 1133 1132 1172 1171 1170 1169 1129 1089 1090 1130 1131 1091 1092 1093 1053 1013 1012 1052 1051 1050 1049 1009 969 929 930 970 1010 1011 971 931 932 972 973 933 934 974 1014 1054 1055 1015 975 935 936 976 1016 1056 1096 1095 1094 1134 1135 1136 1176 1175 1174 1214 1254 1294 1334 1374 1414 1454 1494 1534 1574 1575 1535 1495 1455 1415 1375 1335 1295 1255 1215 1216 1256 1257 1217 1177 1137 1097 1057 1017 977 937 938 978 1018 1058 1098 1138 1178 1218 1258 1298 1297 1296 1336 1376 1416 1456 1496 1576 1536 1457 1417 1377 1337 1338 1378 1379 1339 1299 1259 1219 1179 1139 1099 1059 1019 979 939 940 980 1020 1060 1100 1140 1180 1220 1260 1300 1340 1380 1420 1419 1418 1458 1497 1537 1577 1459 1460 1461 1421 1422 1462 1463 1423 1383 1382 1381 1341 1301 1261 1262 1302 1342 1343 1303 1263 1223 1222 1221 1181 1141 1101 1061 1021 981 941 1142 1182 1183 1184 1224 1264 1304 1344 1384 1385 1425 1424 1464 1465 1466 1467 1468 1428 1388 1348 1347 1387 1427 1426 1386 1346 1345 1305 1265 1266 1306 1307 1308 1268 1267 1227 1226 1225 1185 1186 1187 1228 1188 1148 1147 1146 1145 1144 1143 1102 1062 1022 982 942 818 858 898 943 983 1023 1063 1103 1498 1538 1578 1579 1539 1499 1500 1501 1541 1540 1580 1581 1582 1542 1502 1503 1543 1583 1584 1544 1504 1505 1506 1546 1545 1585 1586 1587 1547 1507 1508 1548 1588 1589 1549 1509 1510 1550 1590 1591 1592 1593 1594 1595 1555 1515 1475 1476 1516 1556 1557 1517 1477 1478 1479 1519 1518 1558 1559 1599 1598 1597 1596 1554 1553 1552 1551 1511 1512 1513 1514 1474 1473 1472 1471 1470 1469 1429 1430 1389 1390 1391 1431 1432 1392 1393 1433 1434 1394 1354 1353 1313 1314 1274 1273 1272 1271 1311 1312 1352 1351 1350 1349 1309 1310 1270 1269 1229 1230 1190 1189 1149 1150 1151 1191 1231 1232 1233 1234 1235 1275 1315 1355 1395 1435 1436 1437 1396 1397 1398 1438 1439 1399 1359 1358 1357 1356 1316 1317 1318 1319 1279 1278 1277 1276 1236 1196 1195 1194 1193 1192 1152 1153 1154 1155 1115 1116 1156 1157 1197 1237 1238 1239 1199 1198 1158 1159 1119 1079 1039 1038 1078 1118 1117 1077 1037 1036 1076 1075 1035 995 994 1034 1114 1074 1073 1113 1112 1072 1032 1033 993 992 952 953 954 955 956 996 997 957 958 998 999 959 919 879 878 918 917 916 915 914 913 912 872 984 1024 1064 1104 944 899 859 819 792 832 833 873 874 834 875 876 877 837 838 839 799 759 719 718 758 798 797 796 836 835 795 794 793 753 752 712 713 714 754 755 756 757 717 716 715 675 674 676 677 678 679 639 638 637 636 635 634 633 673 672 632 592 552 553 593 594 595 554 555 556 596 597 557 558 598 599 559 519 518 517 477 476 516 515 475 474 514 513 512 472 473 433 434 435 436 437 397 398 438 478 479 439 399 359 319 279 278 238 239 199 159 119 118 78 79 39 38 37 77 117 157 158 198 197 237 277 317 318 358 357 356 396 395 394 393 392 432 431 391 351 311 312 352 353 354 355 315 316 276 236 196 195 235 275 274 314 313 273 272 271 232 233 234 194 154 155 156 116 115 75 76 36 35 34 74 114 113 153 193 192 152 112 72 73 33 32 31 71 111 151 191 231 471 511 551 591 631 985 1025 1065 1105 945 900 860 820 779 780 821 861 901 946 986 1026 1066 1106 1107 1108 1068 1067 1027 1028 987 988 671 711 751 791 831 871 911 951 991 1031 1071 1111 1110 1109 1069 1070 1030 1029 989 990 950 949 948 947 906 905 904 903 902 862 822 782 781 739 740 741 742 743 783 784 744 824 823 863 864 865 866 867 907 908 909 910 870 869 868 828 829 830 790 789 788 787 827 826 825 785 786 746 745 705 704 703 702 701 700 699 659 660 661 662 663 664 665 666 706 707 747 748 749 750 710 670 630 30 70 110 150 190 230 590 589 629 628 708 709 669 668 667 627 626 625 624 623 622 621 620 619 579 580 581 582 583 584 585 586 546 547 587 588 548 549 550 510 509 508 507 506 505 545 544 504 543 542 541 540 539 499 500 501 502 503 463 464 465 466 467 468 469 470 430 390 350 310 270 29 69 109 149 189 229 269 309 349 348 388 389 429 428 427 426 425 424 423 422 462 461 460 459 419 420 421 381 380 379 339 340 341 342 382 383 384 385 386 387 347 307 308 268 228 188 148 108 68 28 27 67 107 147 187 227 267 266 306 346 345 344 343 303 302 301 300 299 259 260 261 262 263 264 304 305 265 225 226 186 146 106 105 65 66 26 25 24 64 104 144 145 185 184 224 223 222 221 220 219 179 180 181 182 183 143 103 63 23 22 62 102 142 141 101 61 21 20 60 100 140 139 99 59 19 18 58 98 138 137 177 178 218 217 216 176 136 96 97 17 57 56 16 15 55 95 135 175 215 214 174 213 173 133 134 94 54 14 13 12 52 53 93 92 132 172 212 211 171 131 91 51 11 10 50 90 130 170 210 209 208 168 169 129 89 49 9 8 48 47 7 6 46 86 87 88 128 127 126 166 167 207 206 205 165 125 85 45 5 4 44 43 3 2 42 82 83 84 124 164 204 203 163 123 122 121 81 41 1 0 40 80 120 160 200 201 161 162 202 242 243 244 283 282 322 321 281 241 240 280 320 360 400 440 480 520 521 481 441 442 482 522 523 483 443 403 402 401 361 362 363 323 284 245 285 325 324 364 365 366 326 367 327 287 286 246 247 248 288 328 368 369 329 330 370 371 372 373 333 332 331 291 290 289 249 250 251 252 292 293 253 254 294 334 374 375 376 336 335 295 255 256 296 297 337 377 378 338 298 258 257
116 66 16 15 14 13 12 62 63 113 163 114 115 65 64 164 61 11 111 110 109 60 10 59 9 7 8 58 108 57 6 56 55 156 107 157 106 105 2 4 5 54 104 103 53 3 52 1 0 50 51 100 101 150 200 250 301 300 350 251 201 202 151 102 152 252 302 303 253 153 203 304 254 204 154 155 205 206 255 256 207 257 258 158 208 308 307 306 305 355 354 356 357 359 358 406 454 404 405 456 407 408 409 410 460 510 512 511 561 560 562 611 661 613 563 564 614 612 662 663 713 712 762 711 761 811 812 810 809 759 760 808 758 660 710 659 709 708 555 655 605 457 507 557 508 459 458 509 558 559 506 455 505 556 606 656 657 706 705 704 754 707 757 756 607 608 609 610 658 807 806 856 855 854 906 905 955 954 956 1055 1005 1006 1054 1004 1003 953 902 904 903 853 755 805 804 803 753 852 851 952 951 901 900 850 700 750 800 801 802 752 703 702 603 604 654 653 401 550 500 400 450 451 501 551 453 452 402 352 351 353 403 502 552 553 554 503 504 602 650 600 601 751 701 651 652 1104 1105 1106 1056 1057 1107 1206 1207 1208 1160 1209 1210 1159 1158 1157 1156 1108 1109 1058 1059 907 857 909 859 860 910 911 861 961 960 1011 1060 1010 1061 1110 1111 1062 1112 1113 1163 1162 1312 1262 1263 1212 1161 1260 1259 1261 1211 1213 858 908 958 957 1008 1007 959 1009 862 1012 962 912 863 914 864 913 1120 1119 1121 1170 1220 1270 1269 1319 1321 1320 1471 1472 1522 1373 1423 1372 1422 1470 1420 1370 1421 1371 1369 1419 1619 1569 1519 1469 1520 1521 1571 1570 1621 1620 1169 1268 1318 1219 1218 1168 1167 1217 1166 1216 1164 1214 1264 1165 1215 1265 1118 1116 1117 963 964 1063 1013 1014 1064 1115 1114 1065 1015 1066 1067 1068 1019 1069 1021 1172 1122 1222 1221 1171 1272 1271 1273 1323 1322 1223 1224 1174 1173 1123 1125 1126 1124 1072 1073 1023 1022 972 1020 1070 1071 1018 917 967 1017 1016 916 965 915 865 866 966 969 968 970 971 920 921 922 973 923 872 874 873 870 871 771 821 820 819 919 869 867 868 918 817 818 768 769 766 816 767 718 617 616 666 615 565 514 513 515 468 418 469 467 566 667 717 716 715 665 664 765 815 763 813 814 764 714 668 618 619 670 620 621 571 622 573 574 624 623 673 671 721 720 770 719 669 517 516 466 465 464 211 260 310 311 360 261 210 259 309 209 159 160 161 112 162 213 212 262 312 266 214 264 215 166 216 217 167 165 265 417 368 369 367 416 366 316 315 415 365 364 314 463 411 361 461 412 462 414 413 363 362 313 263 317 318 268 218 269 270 319 421 419 420 422 473 423 472 471 470 570 521 572 523 522 520 519 568 569 567 518 371 373 374 323 372 370 320 225 174 175 275 176 226 223 224 274 273 121 71 72 122 173 172 272 321 267 672 724 723 285 284 34 35 36 85 86 136 84 322 222 221 271 220 219 169 170 171 120 119 168 118 117 67 70 20 21 19 17 18 68 69 722 524 525 526 324 325 276 326 327 277 227 177 279 328 278 228 377 376 375 330 329 280 230 229 331 332 281 381 380 430 431 429 378 379 428 427 424 474 475 425 426 477 476 575 576 626 625 283 233 137 138 87 37 88 89 38 39 134 234 479 478 628 627 676 675 674 577 527 578 528 480 481 482 432 333 184 135 124 24 25 74 23 22 73 123 125 126 75 76 77 26 27 28 78 127 128 178 129 79 130 29 30 80 179 180 131 132 32 31 81 33 83 82 231 181 182 232 282 183 133 334 335 383 740 739 788 738 789 790 791 792 938 382 433 483 533 532 534 683 684 735 685 686 888 841 842 741 742 689 690 640 688 638 639 641 691 692 693 743 643 642 891 840 839 838 937 887 736 633 582 583 634 584 484 434 435 436 437 485 386 336 385 384 585 536 535 588 539 538 537 487 486 687 637 587 586 636 635 632 786 787 737 837 836 886 885 889 890 940 991 941 939 989 987 1036 1037 988 990 1040 1039 1141 1091 1140 1188 1187 1189 1191 1190 1090 1139 1089 1038 1088 1087 1138 1137 682 732 733 734 835 785 784 783 832 834 833 883 884 882 881 933 932 983 982 981 782 831 781 680 681 731 730 729 728 677 678 679 531 530 581 630 631 580 529 579 629 780 779 778 829 830 880 879 930 931 980 928 978 979 929 772 822 823 773 774 775 727 726 725 776 878 828 827 777 825 875 824 826 877 876 926 925 924 974 1074 1025 1075 1024 927 977 1077 1076 1026 975 976 1027 1028 1029 1030 1080 1079 1078 1128 1178 1129 1181 1231 1230 1182 1282 1186 1287 1237 1238 1239 1240 1288 1286 1236 1235 1183 1184 1133 1132 1134 1234 1232 1180 1130 1131 1179 1229 1227 1228 1278 1277 1280 1279 1233 1283 1285 1284 1383 1431 1381 1331 1281 1332 1382 1333 1433 1135 1185 1136 1086 1085 1035 1084 1033 1032 1034 984 934 935 985 986 936 1083 1031 1081 1082 1334 2392 2344 2444 2443 2442 2492 2493 2494 2495 2496 2499 2399 2449 2498 2497 2447 2448 2446 2441 2491 2490 2489 2440 2439 2488 2487 2436 2486 2438 2437 2391 2394 2393 2343 2342 2139 2188 2137 2187 2138 2189 2190 2240 2191 2192 2144 2294 2244 2194 2193 2243 2242 2293 2292 2291 2241 2290 2288 2238 2338 2289 2339 2341 2340 2390 2388 2387 2389 2239 2143 2142 2141 1993 2093 2043 1992 2092 2042 2041 2091 1991 2140 2445 2395 2245 2246 2196 2195 2198 2197 2297 2296 2295 2247 2149 2148 2099 2098 2096 2094 2095 2146 2145 2147 2097 2047 1997 2048 1998 1899 1898 1949 1897 1947 1948 1999 2049 2199 2299 2249 2248 2298 2396 2090 2040 1990 1940 1941 1841 1891 1946 1896 1895 1945 1944 1994 1995 2044 2045 1996 2046 1894 1843 1793 1842 1893 1892 2398 2397 2345 2346 2347 2348 2349 1942 1943 1844 1845 1745 1695 1744 1794 1795 1746 1747 1796 1797 1846 1847 1848 1798 1748 1698 1849 1799 1749 1699 1649 1648 1598 1599 1697 1647 1597 1596 1546 1297 1347 1295 1296 1344 1345 1346 1395 1396 1397 1447 1497 1547 1498 1499 1449 1398 1399 1548 1549 1448 1446 1496 1495 1445 1545 1595 1435 1436 1537 1587 1487 1536 1486 1534 1484 1434 1384 1385 1336 1335 1276 1485 1535 1386 1387 1437 1337 1338 1388 1644 1645 1696 1646 1594 1544 1543 1542 1490 1489 1539 1540 1589 1491 1541 1591 1691 1690 1689 1740 1739 1641 1592 1694 1743 1693 1643 1593 1642 1692 1742 1741 1792 1791 1538 1588 1637 1638 1639 1640 1590 1492 1494 1493 1394 1393 1444 1443 1389 1440 1439 1438 1488 1390 1391 1341 1441 1442 1392 1342 1343 1292 1243 1293 1294 1291 1289 1290 1339 1340 1241 1242 1192 1145 1144 1094 1349 1299 1348 1298 1249 1248 1247 1246 1245 1195 1194 1244 1193 1142 1092 1093 1043 1143 1146 1196 1197 1147 1097 1098 1148 1099 1149 1199 1198 1096 1095 1044 996 1047 1048 1049 997 1046 1045 995 994 993 992 942 1042 1041 945 895 894 946 947 948 899 849 949 999 998 896 845 795 843 892 893 943 944 844 744 694 794 793 846 847 848 897 898 798 797 747 749 799 748 648 548 549 449 498 448 499 599 598 649 698 699 697 597 647 646 695 645 696 746 796 745 596 547 497 546 494 544 594 644 493 590 589 540 287 187 237 286 185 186 235 236 238 188 387 337 338 388 438 389 439 390 391 441 440 490 489 488 491 541 442 443 393 392 492 542 543 593 591 592 444 395 345 394 344 445 545 595 495 496 447 446 295 196 246 296 347 348 297 298 249 299 248 247 48 47 97 148 98 49 99 197 198 199 149 147 46 96 146 243 343 293 294 341 342 291 292 242 241 191 190 140 90 41 40 141 91 42 92 240 239 189 139 290 340 289 288 339 192 142 195 194 244 245 193 143 144 93 44 43 94 45 95 145 346 1326 1930 1931 1929 396 397 398 349 399 1327 1835 1885 1884 1883 1934 1935 1936 2034 2035 1985 1986 2036 2037 2087 2088 2089 2039 1988 1939 1989 1938 1937 1987 2038 1886 1887 1836 1837 1786 1787 1888 1840 1890 1889 1838 1839 1788 1789 1790 1738 1736 1737 1687 1688 1686 1636 1586 1585 1584 1635 1735 1785 1733 1734 1783 1784 1685 1634 1684 1683 1629 1630 1580 1579 1529 1530 1480 1479 1430 1429 1481 1432 1482 1532 1531 1581 1582 1632 1633 1533 1483 1583 1679 1680 1681 1682 1732 1882 1933 1983 1984 1932 1881 1831 1781 1782 1834 1833 1832 1631 1729 1678 1677 1728 1730 1731 1780 1779 1778 1777 1776 1727 1827 1828 1830 1829 1775 1875 1825 1826 1877 1880 1879 1878 1928 1927 1978 2376 2426 2425 2475 2375 2325 2427 2377 2327 2328 2378 2379 2479 2478 2477 2476 2428 2429 2483 2484 2434 2433 2432 2382 2381 2331 2431 2332 2333 2383 2485 2435 2385 2384 2335 2336 2386 2334 2234 2284 2285 2186 2237 2236 2286 2287 2337 2235 2185 2135 2083 2033 2133 2134 2184 2183 2136 2086 2085 2084 2283 2282 2233 2482 2481 2480 2430 2380 2329 2330 2280 2281 2279 2229 2230 2132 2082 2182 1982 1981 2032 2031 2081 2131 2231 2232 2181 2180 2179 2178 2080 2130 2129 2177 2127 2128 2079 2078 2028 2029 2030 1979 1980 2077 2076 2027 1926 1876 1925 1976 1977 2026 2075 2074 2124 2174 2175 2276 2326 2277 2275 2225 2176 2126 2226 2227 2228 2278 2224 2223 2173 2071 2070 2121 2424 2474 2473 2422 2472 2423 2373 2374 2273 2274 2324 2323 2372 2421 2370 2371 2322 2321 2271 2221 2220 2320 2270 2170 2120 2171 2272 2222 2172 2122 2072 2073 2123 2125 2025 1975 1974 2024 2023 2018 1968 1969 2020 2019 2069 1869 1919 1920 1970 1971 2021 2022 1972 1973 1923 1924 1874 1824 1823 1774 1724 1725 1726 1676 1626 1377 1376 1375 1374 1324 1325 1274 1275 1225 1226 1175 1127 1177 1176 1424 1425 1523 1573 1572 1524 1525 1574 1575 1475 1474 1473 1576 1577 1627 1628 1578 1478 1477 1427 1428 1528 1527 1526 1378 1380 1330 1379 1328 1329 1476 1426 1675 1625 1624 1623 1622 1672 1673 1723 1674 1773 1770 1771 1772 1822 1821 1873 1922 1921 1872 1871 1870 1722 1721 1671 1720 1719 1670 1669 1668 1718 1717 1667 1666 1716 1766 1767 1769 1768 1257 1256 1255 1205 1155 1154 1204 1153 1203 1202 1201 1200 1151 1152 1150 1100 1051 1101 1102 1103 1053 1052 1001 1000 1050 950 1002 1254 1304 1305 1306 1356 1350 1400 1351 1300 1250 1301 1252 1251 1401 1352 1402 1451 1452 1502 1501 1403 1404 1405 1355 1354 1303 1253 1302 1353 1307 1357 1258 1308 1406 1407 1408 1358 1458 1456 1506 1507 1457 1656 1706 1510 1560 1559 1509 1508 1609 1608 1658 1657 1557 1505 1555 1605 1455 1454 1453 1558 1606 1556 1607 1707 1708 1709 1710 1513 1563 1516 1567 1617 1616 1618 1518 1517 1568 1566 1565 1665 1615 1564 1614 1613 1562 1561 1511 1463 1462 1512 1461 1459 1460 1409 1359 1360 1410 1413 1412 1411 1611 1612 1662 1663 1712 1760 1759 1758 1810 1860 1711 1713 1361 1362 1468 1467 1367 1266 1267 1317 1368 1418 1417 1314 1315 1365 1366 1316 1415 1416 1466 1465 1515 1514 1464 1414 1364 1363 1313 1311 1310 1309 1714 1763 1764 1814 1813 1765 1715 1664 1761 1762 1812 1811 1661 1659 1660 1610 1864 1861 1862 1863 1817 1818 1868 1917 1918 1867 1820 1819 1816 1815 1866 1916 1865 1914 1913 1912 1910 1911 1915 1966 2067 2068 2017 1967 1965 2014 2015 2116 2119 2118 2117 2066 2016 2065 2115 2064 2114 2165 2164 2113 2063 2163 2214 2215 2265 2216 2367 2418 2468 2467 2417 2368 2318 2319 2369 2419 2471 2470 2420 2469 2317 2267 2266 2166 1964 1963 1962 2013 2062 2012 1961 2011 1960 1959 2009 2109 2059 2060 2010 2008 2217 2218 2169 2219 2268 2269 2168 2167 2316 2315 2264 2314 2312 2313 2363 2362 2365 2364 2416 2366 2465 2466 2415 2414 2263 2211 2261 2262 2212 2213 2110 2111 2061 2161 2112 2162 2058 2108 2106 2057 2056 2107 2158 2159 2208 2410 2460 2459 2462 2461 2464 2463 2413 2412 2411 2361 2310 2311 2360 2359 2309 2409 2458 2408 2358 2308 2259 2258 2457 2407 2257 2307 2357 2207 2209 2160 2260 2210 2157 2206 2256 2306 2356 2406 2405 2355 2255 2254 2305 2304 2354 2303 2253 2203 2204 2353 2403 2404 2455 2451 2450 2401 2400 2350 2351 2452 2402 2352 2453 2454 2456 2205 2156 2155 2105 2104 2154 2153 2052 2051 2002 2055 2005 2006 1956 1955 1909 1859 1858 1908 2007 1957 1958 1809 1808 1807 1907 1857 1905 2054 2053 2103 2102 2101 2151 2152 2202 2201 2200 2150 2100 2050 2300 2250 2251 2301 2252 2302 2003 1953 2004 1954 1902 1952 1901 1950 2001 2000 1951 1903 1855 1906 1856 1806 1756 1757 1754 1755 1705 1654 1655 1704 1703 1753 1701 1702 1603 1553 1552 1604 1503 1504 1554 1653 1650 1651 1652 1551 1600 1550 1450 1500 1601 1602 1752 1751 1700 1750 1851 1852 1800 1900 1850 1801 1802 1853 1803 1805 1804 1854 1904
200 150 100 50 0 1 51 101 151 201 251 250 300 301 302 252 202 152 102 103 53 52 2 3 4 54 104 154 153 203 204 254 253 303 304 354 353 352 351 350 400 450 500 550 600 601 551 501 451 401 402 452 502 552 602 652 651 650 700 750 751 701 702 752 753 703 653 603 553 503 453 403 404 454 504 554 604 654 704 957 907 857 807 757 707 706 756 806 805 856 906 956 955 954 904 905 855 854 804 754 755 705 655 656 657 607 557 507 506 556 606 605 555 505 455 405 355 356 406 456 457 407 357 307 257 256 306 305 255 205 155 156 206 207 157 107 57 56 106 105 55 5 6 7 8 58 59 9 10 60 61 11 12 62 112 111 110 109 108 158 159 160 161 162 212 211 210 209 208 258 308 358 408 409 359 309 259 260 261 262 312 311 310 360 361 362 412 462 512 562 561 511 461 411 410 460 510 560 559 509 459 458 508 558 608 658 659 609 610 611 612 661 660 710 709 708 758 759 760 761 762 812 811 711 712 662 663 713 763 813 863 862 861 860 810 809 808 858 859 909 908 958 959 960 910 911 961 962 912 913 963 964 914 864 814 764 714 664 614 613 563 564 514 513 463 413 464 414 364 363 313 263 213 163 113 63 13 14 15 65 64 114 115 165 164 214 215 265 264 314 315 365 415 465 515 565 615 665 715 765 815 865 915 965 966 967 917 916 866 816 766 716 717 718 768 767 867 817 818 868 918 968 969 919 869 819 769 719 720 670 669 668 667 666 616 617 618 568 567 566 516 466 416 366 367 417 467 517 518 468 469 519 569 619 620 570 520 470 420 419 418 368 318 317 316 266 267 268 218 168 167 217 216 166 116 66 16 17 18 19 69 68 67 117 118 119 169 219 269 319 369 370 320 270 220 170 120 70 20 21 22 23 24 74 124 73 72 71 121 171 172 122 123 173 174 224 223 222 221 271 321 371 421 471 674 673 672 671 721 771 770 820 870 970 920 821 822 772 722 723 773 823 824 825 775 774 724 725 726 776 826 827 777 727 677 627 626 676 675 625 624 623 622 621 521 571 572 522 472 473 423 422 372 322 272 273 274 324 323 373 374 424 474 524 523 573 574 575 525 526 576 577 527 477 476 475 425 375 376 426 427 377 327 326 276 277 227 226 176 177 127 126 76 77 26 25 75 125 175 225 275 325 871 921 971 972 922 872 877 878 879 880 881 882 883 884 934 933 983 984 1034 1084 1134 1133 1184 1234 1284 1283 1233 1183 1232 1282 1182 1132 1082 1083 1033 1032 982 932 931 930 929 928 927 926 876 875 874 873 923 973 974 924 925 975 976 977 978 1028 1029 979 980 981 1031 1030 1080 1081 1131 1130 1129 1079 1078 1077 1027 1026 1025 1024 1023 1022 1021 1020 1070 1071 1072 1073 1074 1075 1076 1126 1127 1128 1178 1179 1180 1181 1231 1281 1280 1230 1229 1279 1228 1278 1277 1227 1177 1176 1226 1276 1275 1225 1175 1125 1124 1123 1122 1121 1120 1170 1220 1221 1171 1172 1222 1223 1173 1174 1224 1274 1273 1272 1271 1270 1320 1370 1420 1470 1471 1421 1371 1321 1322 1372 1373 1323 1324 1374 1424 1423 1422 1472 1522 1521 1520 1570 1571 1621 1620 1670 1671 1721 1720 1722 1723 1724 1725 1675 1674 1673 1672 1622 1572 1573 1523 1473 1474 1524 1574 1623 1624 1625 1575 1525 1475 1425 1375 1325 1326 1376 1426 1476 1526 1576 1577 1627 1626 1676 1726 1727 1677 1678 1728 1729 1679 1680 1730 1332 1382 1432 1482 1532 1582 1632 1682 1732 1731 1681 1631 1630 1629 1628 1578 1579 1529 1528 1527 1477 1478 1428 1427 1377 1378 1379 1380 1430 1429 1479 1480 1530 1580 1581 1531 1481 1431 1381 1331 1330 1329 1328 1327 27 1719 1669 1619 1569 1568 1618 1668 1718 1717 1716 1666 1667 1617 1567 1517 1518 1519 1469 1468 1467 1516 1466 1465 1515 1565 1566 1616 1615 1665 1715 1765 1815 1816 1766 1767 1817 1818 1868 1867 1866 1865 1915 1916 1917 1967 1968 1918 1919 1869 1870 1920 1970 1969 2019 2018 2017 2016 1966 1965 2015 2065 2115 2066 2067 2068 2069 2070 2020 1820 1819 1768 1417 1418 1419 1369 1368 1367 1317 1316 1366 1416 1415 1365 1315 1265 1266 1267 1268 1318 1319 1269 1219 1169 1119 1118 1068 1069 1019 1018 1017 1016 1015 1065 1066 1067 1117 1116 1166 1167 1168 1218 1217 1216 1215 1214 1213 1163 1164 1165 1115 1114 1064 1014 1013 1012 1062 1063 1113 1112 1111 1061 1011 1010 1060 1059 1009 1008 1058 1108 1109 1110 1160 1161 1162 1212 1211 1210 1209 1159 1158 1208 1258 1259 1260 1261 1262 1312 1313 1263 1264 1314 1769 1770 1364 1414 1413 1363 1362 1412 1411 1361 1311 1310 1360 1410 1409 1359 1309 1308 1358 1408 1007 1057 1107 1157 1207 1257 1307 1357 1407 1457 1458 1459 1460 1461 1462 1512 1511 1561 1562 1560 1510 1509 1508 1507 1557 1607 1608 1558 1559 1609 1610 1611 1612 1613 1563 1513 1463 1464 1514 1564 1614 1664 1663 1662 1712 1711 1661 1660 1659 1658 1657 1707 1708 1709 1710 1760 1759 1758 1757 1807 1808 1809 1810 1811 1761 1762 1763 1713 1714 1764 1814 1864 1914 1964 1963 1913 1863 1813 1812 1862 1912 1911 1861 1860 1859 1858 1857 1907 1908 1958 1957 1959 1909 1910 1960 1961 1962 2012 2062 2063 2013 2014 2064 2114 2113 2112 2111 2061 2011 2010 2060 2110 2116 2109 2059 2009 2008 2007 2006 2005 2004 1954 1955 1956 1906 1905 1904 1854 1804 1805 1855 1856 1806 1756 1755 1754 1704 1654 1655 1705 1706 1656 1606 1556 1555 1605 1604 1554 1504 1505 1506 1456 1455 1454 1404 1405 1406 1356 1306 1305 1355 1354 1304 1254 1255 1256 1206 1156 1106 1105 1055 1056 1006 1005 1004 1054 1104 1154 1155 1205 1204 1103 1053 1003 1002 1052 1102 1101 1051 1001 951 952 953 903 853 803 802 801 800 850 851 852 902 901 900 950 1000 1050 1100 1150 1151 1152 1153 1203 1253 1252 1202 1201 1200 1250 1251 1301 1300 1350 1400 1401 1351 1352 1302 1303 1353 1403 1402 1452 1453 1451 1450 1500 1550 1551 1501 1502 1552 1602 1601 1600 1650 1651 1652 1702 1701 1700 1750 1751 1752 1802 1852 1851 1801 1800 1850 1900 1901 1951 1950 2000 2001 2002 2003 1953 1952 1902 1903 1853 1803 1753 1703 1653 1603 1553 1503 2058 2108 2107 2057 2056 2106 2105 2055 2054 2104 2154 2204 2254 2304 2452 2402 2401 2451 2450 2400 2350 2351 2301 2300 2250 2251 2201 2200 2150 2151 2101 2100 2050 2051 2052 2053 2103 2102 2152 2153 2203 2202 2252 2253 2303 2302 2352 2353 2403 2453 2454 2455 2405 2404 2354 2355 2305 2255 2205 2155 2156 2157 2207 2206 2256 2306 2356 2406 2456 2457 2458 2408 2407 2357 2358 2308 2307 2257 2258 2208 2158 2159 2160 2161 2162 2163 2164 2165 2166 1771 2117 2167 2217 2216 2215 2214 2213 2212 2211 2210 2209 2259 2309 2310 2260 2261 2262 2263 2313 2312 2311 2361 2360 2359 2409 2459 2460 2410 2411 2461 2462 2463 2413 2412 2362 2363 2364 2414 2464 2465 2415 2365 2315 2314 2264 2265 2266 2316 2317 2267 2218 2219 2169 2168 2118 2119 2120 2170 2220 2270 2269 2268 2318 2368 2367 2366 2416 2466 2467 2417 2418 2468 2469 2419 2369 2319 2320 2370 2420 2470 2471 2472 2473 2423 2422 2421 2371 2321 2271 2272 2273 2274 2324 2323 2322 2372 2373 2374 2424 2474 2475 2425 2375 2325 2275 2225 2224 2223 2173 2174 2172 2222 2221 2171 2121 2122 2123 2124 2175 2125 2126 2176 2177 2127 2128 2178 2228 2278 2328 2327 2277 2227 2226 2276 2326 2376 2377 2378 2428 2427 2426 2476 2477 2478 2479 2429 2379 2329 2279 2229 2179 2129 2130 2180 2230 2280 2281 2231 2331 2330 2380 2430 2480 2481 2431 2381 2382 2432 2482 2483 2484 2434 2433 2383 2333 2332 2282 2232 2181 2131 2132 2182 2183 2133 2134 2184 2234 2233 2283 2284 2334 2384 2385 2435 2485 2486 2436 2386 2336 2335 2285 2235 2185 2135 2074 2073 2072 2071 2021 2022 1972 1971 1921 1821 1871 1872 1922 1923 1973 2023 2024 1974 1924 1874 1873 1823 1822 1772 28 29 1773 1824 1774 1775 1825 1875 1925 1975 2025 2075 2076 2077 2027 2026 1976 1926 1927 1977 1978 1928 1878 1877 1876 1826 1776 1777 1827 1828 1778 1779 1829 1879 1929 1979 2029 2028 2078 2079 2080 2081 2031 2030 1980 1981 1931 1930 1880 1881 1831 1830 1780 1781 1782 1832 1882 1932 1982 2032 2082 2083 2033 2034 2084 2286 2236 2186 2136 2086 2085 2035 1985 1984 1983 1933 1934 1935 1885 1884 1883 1833 1783 1784 1834 1835 1785 1786 1836 1886 1936 1986 2036 2037 1987 2087 2137 2187 2237 2287 2337 2387 2437 2487 2488 2489 2439 2438 2388 2338 2389 2339 2340 2390 2440 2490 2491 2441 2391 2341 2289 2288 2188 2238 2239 2189 2139 2138 2088 2089 2039 2038 1988 1938 1937 1887 1837 1787 1788 1789 1790 1840 1839 1838 1888 1889 1890 1940 1939 1989 1990 2040 2090 2140 2190 2240 2290 2291 2342 2392 2442 2492 2493 2443 2444 2494 2495 2445 2395 2345 2344 2394 2393 2343 2293 2292 2241 2242 2243 2192 2191 2141 2091 2041 1991 1941 1891 1841 1791 1792 1842 1892 1942 1992 2042 2092 2142 2143 2193 2194 2244 2294 2295 2245 2195 2196 2246 2296 2346 2396 2397 2398 2448 2447 2446 2496 2497 2498 2499 2449 2399 2349 2348 2347 2297 2298 2299 2249 2248 2247 2197 2198 2199 2149 2148 2147 2146 2145 2144 2093 2043 1993 1943 1893 1843 1793 1794 1844 1845 1895 1894 1944 1994 2044 2094 2095 2096 2097 2098 2099 2049 2048 2047 2046 2045 1995 1945 1946 1996 1997 1998 1999 1949 1899 1849 1799 1798 1848 1898 1948 1947 1897 1896 1846 1847 1797 1747 1746 1796 1795 1745 1744 1743 1693 1694 1695 1696 1697 1698 1748 1749 1699 1649 1648 1647 1646 1645 1644 1643 1642 1692 1742 1741 1691 1641 1591 1592 1593 1594 1595 1596 1597 1598 1599 1549 1548 1547 1546 1545 1544 1543 1542 1541 1540 1590 1640 1690 1740 1739 1738 1737 1736 1686 1687 1688 1689 1639 1589 1539 1538 1588 1638 1637 1636 1586 1587 1537 1536 1585 1635 1685 1735 1734 1684 1683 1733 1633 1634 1584 1583 1533 1483 1433 1383 1333 1334 1384 1434 1484 1534 1535 1485 1435 1436 1486 1487 1488 1489 1490 1440 1439 1438 1437 1387 1386 1385 1335 1336 1337 1338 1388 1389 1390 1339 1340 79 78 1341 1391 1441 1491 1492 1442 1443 1493 1494 1495 1444 1445 1446 1496 1497 1498 1499 1449 1448 1447 1397 1347 1348 1398 1399 1349 1299 1298 1297 1296 1346 1396 1395 1394 1393 1392 1342 1343 1344 1345 1295 1245 1246 1247 1248 1249 1199 1198 1149 1148 1147 1197 1196 1195 1194 1244 1294 1293 1292 1291 1290 1289 1288 1287 1238 1239 1240 1241 1242 1243 1193 1192 1143 1144 1094 1095 1145 1146 1096 1097 1098 1099 1049 1048 1047 1046 1045 995 996 997 998 999 949 948 947 946 945 944 943 993 994 1044 1043 1093 1142 1141 1191 1190 1189 1188 1187 1237 1236 1286 1285 1235 1185 1186 1136 1135 1085 1086 1087 1137 1138 1088 1089 1139 1140 1090 1091 1092 1042 992 942 941 991 1041 1040 1039 989 990 940 939 938 988 1038 1037 1036 1035 985 986 987 937 936 935 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 849 848 798 799 749 748 747 797 847 846 796 746 696 697 698 699 649 648 647 646 645 695 745 795 845 844 843 793 794 744 743 693 694 644 643 593 543 544 594 595 545 546 596 597 547 548 598 599 549 499 449 399 349 299 298 248 249 199 149 99 49 48 98 148 198 348 398 448 498 497 447 446 496 495 445 395 396 397 347 346 345 295 296 297 247 197 196 246 245 244 294 344 394 444 494 493 443 393 343 293 243 193 143 93 94 144 194 195 145 146 147 97 47 46 96 95 45 44 43 42 41 40 90 140 141 91 92 142 192 242 292 291 241 191 190 240 290 128 129 289 339 340 341 342 392 391 390 440 441 442 492 491 490 540 541 542 592 591 590 640 690 691 641 642 692 742 741 740 790 791 792 842 841 840 839 789 739 689 639 589 539 489 439 389 239 189 139 89 39 38 37 36 35 85 86 136 135 185 186 236 237 187 137 87 88 138 188 238 288 287 286 285 235 234 184 134 84 34 33 32 31 30 80 81 131 130 180 181 182 132 82 83 133 183 233 232 231 230 229 179 178 228 278 279 280 281 282 283 284 334 335 336 337 338 388 387 386 385 384 383 333 332 331 330 329 328 378 379 380 381 382 432 433 434 435 436 437 438 488 487 486 485 484 483 534 535 536 537 538 588 638 688 738 788 838 837 787 737 687 686 636 637 587 586 585 584 583 533 532 482 481 431 430 429 428 478 528 529 479 480 530 531 581 580 582 632 633 683 684 634 635 685 736 786 836 835 785 735 734 784 834 833 783 733 732 682 681 631 630 629 579 578 628 678 679 680 731 781 782 832 831 830 780 730 729 728 778 779 829 828
8019 8119 8120 8020 7920 7921 8021 8121 8221 8220 8219 8319 8320 8321 8421 8420 8419 8418 8318 8218 8217 8317 8417 8416 8316 8216 8215 8315 8415 8414 8314 8214 8114 8115 8116 8117 8118 8018 8017 7917 7916 8016 8015 7915 7815 7715 7615 7617 7616 7716 7816 7817 7717 7718 7818 7918 7919 7819 7719 7720 7820 7821 7721 7621 7521 7520 7620 7618 7619 7519 7518 7517 7516 7416 7415 7515 7514 7614 7714 7814 7914 8014 8113 8013 7913 7813 7713 7613 7513 7414 7413 7313 7314 7214 7215 7315 7316 7317 7417 7418 7419 7420 7421 7321 7320 7220 7221 7121 7120 7119 7219 7319 7318 7218 7118 7018 7019 7017 7117 7217 7216 7116 7115 7114 7113 7213 7212 7312 7412 7512 7612 7712 7812 7912 8012 8112 8212 8213 8413 8313 8312 8412 8411 8311 8211 8111 8011 7911 7811 7711 7611 7511 7411 7311 7211 7111 7112 7012 7013 7014 7015 7016 6816 6815 6814 6813 6812 6811 7011 6911 6912 6913 6914 6915 6916 6917 6918 6919 7020 7021 6921 6920 6820 6819 6817 6818 6618 6518 6517 6617 6616 6516 6416 6417 6418 6419 6420 6520 6519 6619 6620 6720 6719 6718 6717 6716 6715 6714 6614 6615 6515 6415 6514 6414 6413 6513 6512 6412 6411 6511 6610 6611 6612 6613 6713 6712 6711 6710 6810 6809 6709 6708 6608 6609 6509 6510 6410 6409 6408 6508 6507 6407 6406 6506 6606 6607 6707 6807 6808 6908 6909 6910 7010 7110 7210 7310 7410 7510 7610 7710 7810 7910 8010 8110 8210 8310 8410 8409 8309 8209 8109 8009 7909 7809 7709 7609 7509 7409 7309 7209 7109 7009 7008 7007 6907 6906 6905 6805 6806 6706 6705 6605 6505 6405 6404 6403 6402 6401 6400 6500 6501 6502 6503 6504 6604 6704 6804 6803 6703 6603 6602 6601 6600 6700 6800 6801 6701 6702 6802 6902 6903 6904 7005 7006 7004 7003 7002 7001 6901 6900 7000 7100 7200 7300 7201 7101 7102 7202 7203 7103 7104 7105 7106 7107 7108 7208 7308 7408 7508 7608 7708 7707 7607 7507 7407 7307 7306 7305 7405 7404 7403 7402 7401 7301 7302 7303 7304 7204 7205 7207 6621 6521 6421 6422 6522 6622 6721 6821 7206 7406 7506 7606 7706 7806 7807 7808 7908 8008 8108 8208 8308 8408 8407 8307 8207 8107 8007 7907 7906 7805 7705 7605 7505 7504 7604 7704 7804 7803 7903 7802 7801 7701 7601 7602 7702 7703 7603 7503 7502 7501 7400 7500 7600 7700 7800 7900 7901 7902 8002 8003 8004 7904 7905 8005 8006 8106 8105 8205 8206 8306 8406 8405 8305 8304 8404 8403 8402 8401 8301 8302 8303 8203 8204 8104 8103 8102 8202 8201 8101 8001 8000 8100 8200 8300 8400 8500 8600 8601 8501 8502 8602 8702 8703 8603 8503 8504 8505 8605 8604 8704 8705 8805 8804 8803 8903 8904 9003 9002 8902 8802 8801 8701 8700 8800 8900 8901 9001 9000 9100 9101 9201 9202 9102 9103 9203 9204 9104 9004 8905 8906 8806 8706 8606 8506 8507 8607 8707 8807 8907 9007 9107 9106 9006 9005 9105 9205 9305 9304 9303 9302 9402 9403 9502 9602 9702 9701 9700 9600 9500 9400 9300 9200 9301 9401 9501 9601 9800 9900 9901 9801 9802 9902 9903 9803 9703 9704 9604 9603 9503 9504 9404 9405 9406 9306 9206 9207 9307 9407 9507 9607 9606 9506 9505 9605 9705 9706 9707 9807 9806 9805 9804 9904 9905 9906 9907 9908 9808 9708 9709 9809 9909 9910 9810 9710 9610 9609 9608 9508 9509 9510 9410 9411 9409 9408 9308 9208 9108 9109 9209 9309 9310 9210 9211 9311 9511 9611 9711 9811 9911 9912 9812 9712 9612 9512 9412 9312 9212 9112 9111 9110 9010 8910 8909 9009 9008 8908 8808 8708 8608 8508 8509 8609 8709 8809 8810 8710 8610 8510 8511 8611 8711 8811 8911 9011 9012 9013 9014 9114 9214 9314 9315 9215 9115 9113 9213 9313 9413 9414 9415 9515 9514 9513 9613 9614 9714 9713 9813 9913 9914 9814 9815 9915 9916 9816 9716 9715 9615 9616 9516 9416 9316 9216 9116 9016 9015 8914 8915 8815 8814 8813 8913 8912 8812 8712 8612 8512 8513 8514 8614 8613 8713 8714 8715 8615 8515 8516 8517 8518 8620 8720 8820 8821 8721 8621 8521 8520 8519 8619 8618 8617 8616 8716 8717 8718 8719 8819 8818 8817 8816 8916 8917 9017 9018 8918 9118 9117 9217 9317 9417 9517 9617 9717 9817 9917 9918 9818 9718 9618 9518 9418 9318 9218 9219 9119 9019 8919 8920 8921 9021 9020 9120 9121 9221 9220 9320 9321 9421 9521 9520 9420 9319 9419 9519 9619 9719 9819 9919 9920 9820 9720 9620 9621 9721 9821 9921 9922 9923 9823 9822 9722 9622 9522 9422 9423 9424 9524 9523 9623 9723 9724 9624 9824 9924 9925 9825 9725 9726 9728 9828 9928 9927 9926 9826 9827 9727 9626 9625 9525 9526 9426 9425 9325 9324 9323 9322 9222 9223 9123 9122 9022 9023 9024 9124 9224 9225 9226 9326 9327 9427 9527 9627 9628 9528 9428 9328 9228 9227 9127 9126 9125 9025 8925 8924 8923 8922 8722 8822 8823 8723 8623 8622 8522 8523 8524 8624 8625 8525 8526 8527 8528 8529 8530 6423 6523 6623 6722 6822 8630 8629 8628 8728 8828 9128 9027 8927 8827 8727 8627 8626 8726 8725 8724 8824 8825 8826 8926 9026 9028 8928 8929 8829 8729 8730 8830 8930 9029 9129 9229 9329 9429 9529 9629 9729 9829 9929 9930 9830 9730 9630 9530 9430 9330 9230 9130 9030 9031 9131 9132 9232 9231 9331 9332 9432 9431 9531 9532 9632 9631 9731 9732 9733 9833 9832 9831 9931 9932 9933 9934 9935 9936 9836 9835 9834 9734 9735 9635 9634 9633 9533 9433 9434 9534 9535 9536 9636 9736 9737 9837 9937 9938 9838 9738 9739 9839 9939 9940 9941 9841 9840 9740 9741 9641 9640 9639 9638 9637 9537 9538 9539 9540 9541 9441 9440 9439 9438 9437 9436 9435 9334 9333 9233 9133 8933 8833 8832 8732 8731 8831 8931 8932 9032 9033 9034 9035 9135 9134 9234 9235 9136 9036 8936 8935 8934 8834 8734 8733 8633 8632 8631 8531 8532 8533 8534 8634 8635 8735 8835 8836 8736 8737 8738 8838 8837 8937 8938 9038 9037 9137 9138 9238 9338 9337 9237 9236 9336 9335 9442 9542 9543 9443 9444 9544 9545 9445 9645 9644 9643 9642 9742 9743 9843 9842 9942 9943 9944 9844 9744 9745 9845 9945 9946 9947 9847 9846 9746 9646 9546 9446 9447 9448 9548 9547 9747 9647 9648 9748 9749 9849 9850 9750 9650 9649 9549 9449 9450 9550 9551 9451 9452 9453 9454 9553 9552 9652 9651 9751 9851 9951 9950 9949 9948 9848 9339 9340 9341 9342 9241 9240 9239 9139 9039 8939 8940 8941 8942 8943 9043 9143 9141 9140 9040 9041 9042 9142 9242 9243 9343 9344 9345 9245 9244 9144 9145 9045 9044 8944 8945 8845 8844 8843 8842 8841 8741 8740 8840 8839 8739 8638 8637 8636 8535 8536 8436 8435 8434 8334 8333 8433 8432 8332 8232 8233 8234 8235 8335 8336 8337 8338 8437 8537 8538 8438 8439 8539 8639 8640 8641 8541 8540 8440 8441 8341 8340 8339 8239 8240 8241 8242 8342 8442 8542 8642 8742 8743 8643 8644 8744 8745 8645 8545 8544 8543 8443 8444 8445 8345 8344 8343 8243 8244 8245 8145 8045 8044 8144 8143 8043 8142 8141 8140 8139 8138 8238 8236 8237 8137 8136 8135 8134 8133 8132 8231 8331 8431 8430 8429 8428 8427 8426 8425 8424 8423 8422 7822 7722 7622 7522 7422 7322 7222 7122 7022 6922 6923 6823 6723 6724 6624 6524 6424 6425 6525 6625 6725 6825 6824 6924 6925 7025 7024 7023 7123 7223 7323 7423 7523 7623 7624 7524 7724 7723 7823 7824 7924 8024 8023 7923 7922 8022 8122 8123 8124 8224 8223 8222 8322 8323 8324 8325 8225 8226 8326 8327 8328 8329 8330 8230 8131 8130 8129 8229 8228 8227 8128 8127 8126 8125 8025 7925 7825 7826 7726 7725 7625 7525 7425 7424 7324 7224 7124 7125 7225 7325 7326 7426 7626 7526 7527 7627 7727 7827 7828 7928 7927 7926 8026 8027 8028 8029 7929 7930 8030 8031 8032 8033 8034 8035 8036 8037 8038 8039 8040 8041 8042 7945 7944 7943 7942 7941 7940 7939 7932 7931 7831 7832 7732 7731 7730 7830 7829 7729 7728 7628 7528 7427 7327 7227 7226 7126 7127 7027 7026 6926 6826 6726 6626 6526 6426 6427 6527 6627 6727 6827 6927 6928 7028 7128 7228 7328 7428 7429 7430 7530 7529 7629 7630 7631 7632 7633 7733 7833 7933 9554 9653 9752 7934 7834 7835 7935 7936 7937 7938 7839 7840 7841 7842 7838 7837 7836 7736 7636 7635 7735 7734 7634 7534 7533 7532 7531 7431 7330 7329 7229 7129 7029 6929 6828 6829 6729 6728 6628 6629 6529 6528 6428 6429 6430 6530 6630 6730 6830 6930 7030 7130 7230 7331 7332 7432 7433 7434 7435 7535 7536 7436 7437 7537 7637 7737 7738 7638 7538 7438 7439 7539 7639 7739 7740 7741 7742 7743 7843 7844 7845 7745 7744 7644 7645 7643 7642 7542 7541 7641 7640 7540 7440 7441 7442 7342 7443 7543 7544 7545 7444 7445 7345 7344 7343 7243 7244 7245 7145 7144 7143 7142 7242 7341 7340 7240 7241 7141 7140 7139 7239 7339 7338 7238 7138 7137 7237 7337 7336 7335 7236 7136 7135 7235 7234 7334 7333 7233 7232 7231 7131 7031 7032 7132 7133 7134 7034 7033 6933 6932 6931 6831 6731 6732 6832 6833 6733 6734 6834 6934 6935 6835 7035 7036 7037 7038 7039 7040 7041 7042 7043 6943 6843 6844 6944 7044 7045 6945 6845 6745 6744 6743 6643 6644 6645 6545 6544 6543 6542 6642 6742 6741 6841 6842 6942 6941 6940 6840 6839 6939 6938 6838 6837 6937 6936 6836 6736 6735 6635 6535 6435 6434 6534 6634 6633 6632 6631 6531 6532 6533 6433 6333 6332 6432 6431 6331 6231 6232 6233 6234 6334 6335 6235 6135 6134 6133 6132 6131 6031 6032 6033 6034 6035 6036 6136 6236 6336 6436 6536 6636 6738 6739 6740 6540 6539 6639 6640 6641 6541 6441 6440 6340 6341 6241 6242 6243 6343 6342 6442 6443 6444 6445 6345 6344 6244 6144 6143 6043 5943 5942 6042 6142 6141 6140 6240 6239 6439 6339 6338 6438 6538 6638 6737 9654 9753 9852 9952 6637 6537 6437 6337 6237 6238 6138 6137 6139 6039 5939 5940 6040 6041 5941 5841 5840 5740 5741 5641 5640 5639 5638 5738 5739 5839 5838 5938 6038 6037 5937 5837 5737 5637 5537 5538 5539 5540 5541 5542 5642 5742 5842 5843 5743 5643 5744 5745 5845 5844 5944 6044 6045 5945 5946 5846 5746 5646 5647 5747 5847 5947 6047 6046 6146 6145 6245 6246 6346 6347 6247 6147 6148 6248 6048 5948 5848 5748 5648 5548 5547 5546 5545 5645 5644 5544 5543 5442 5441 5440 5340 5338 5238 5237 5337 5437 5438 5439 5339 5239 5240 5241 5341 5342 5242 5142 5143 5243 5343 5443 5444 5445 5446 5447 5448 5348 5248 5148 5048 5047 5046 5146 5147 5247 5347 5346 5246 5245 5345 5344 5244 5144 5145 5045 5044 5043 5042 5041 5141 5140 5139 5039 5040 4940 4939 4938 4937 5037 5038 5138 5137 5136 5936 5935 5934 5933 5932 5931 5831 5832 5833 5234 5134 5034 4934 4834 4835 4935 5035 5135 5235 5236 5036 4936 4836 4837 4838 4738 4737 4736 4735 4734 4634 4635 4636 4637 4638 4639 4539 4538 4537 4536 4535 4435 4335 4336 4436 4437 4438 4439 4440 4540 4640 4740 4739 4839 4840 4841 4941 4942 4842 4843 4943 4944 4945 4946 4846 4845 4844 4744 4743 4742 4741 4641 4642 4542 4541 4441 4442 4443 4543 4643 4644 4544 4545 4546 4646 4645 4745 4746 4747 4847 4947 6446 6447 6448 6348 4948 4848 4748 4648 4647 4547 4548 4448 4447 4446 4445 4444 4344 4343 4342 4341 4340 4339 4338 4337 4334 4434 4534 6230 6330 6329 6229 5631 5731 5732 5733 5734 5834 5836 5835 5735 5736 5636 5536 5436 5336 5335 5334 5434 5435 5535 5635 5634 5534 5533 5633 5632 5532 5531 5431 5432 5433 5333 5233 5232 5332 5331 5231 5131 5132 5133 5033 5032 5031 4931 4831 4832 4932 4933 4833 4733 4732 4632 4633 4533 4532 4432 4433 4333 4332 4331 4431 4531 4530 4630 4631 4731 4730 4830 5030 5029 5129 5130 5230 5330 5430 5429 5329 5229 5228 5128 5028 4928 4930 4929 4829 4828 4728 4729 4629 4628 4528 4529 4430 4330 4329 4429 4428 4328 4327 4326 4426 4427 4527 4627 4727 4827 4826 4926 4927 5027 5026 5126 5127 5227 5327 5328 5428 5427 5527 5528 5628 5728 5729 5629 5529 5530 5630 5730 5830 5930 6030 6130 6129 6029 6028 6128 6228 6328 6327 6227 6127 6027 5927 5928 5929 5829 5828 5827 5826 5726 5727 5627 5626 5526 5426 5326 5226 5225 5125 5025 4925 4825 4725 4726 4626 4526 4625 4525 4425 4325 4324 4424 4524 4624 4724 4824 4924 5024 5124 5224 5325 5425 5725 5825 6025 6125 6126 6026 5926 5925 5924 5824 5724 5624 5625 5525 5524 5424 5324 5323 5423 5523 5623 5723 5823 5923 5922 6022 6023 6024 6124 6224 6225 6226 6326 6325 6324 6323 6223 6123 6122 6121 6120 6020 6019 6119 6219 6220 6320 6319 6321 6322 6222 6221 6021 5921 5821 5721 5621 5622 5722 5822 5820 5920 5919 5918 6017 6018 6118 6117 6217 6218 6318 6317 6316 6216 6116 6016 5916 5917 5817 5818 5819 5720 5620 5521 5522 5422 5322 5222 5223 5123 5023 4923 4823 4723 4722 4822 4922 5022 5122 5121 5021 5221 5321 5421 5520 5519 5619 5719 5718 5717 5617 5618 5518 5418 5419 5420 5320 5220 5120 5119 5219 5319 5318 5317 5417 5517 5516 5616 5716 5816 5815 5915 6015 6014 6013 6113 6213 6214 6114 6115 6215 6315 6314 6313 6312 6212 6112 6012 5912 5913 5914 5814 5813 5812 5712 5713 5613 5714 5715 5615 5614 5514 5515 5416 5316 5216 5217 5218 5118 5117 5017 5018 5019 5020 4920 4921 4821 4721 4621 4622 4623 4523 4423 4323 4522 4521 4620 4720 4820 4819 4919 4918 4818 4917 4916 5016 5116 5115 5215 5315 5415 5414 5314 5214 5213 5313 5413 5513 5612 5512 5412 5312 5212 5311 5411 5511 5611 5711 5811 5911 5910 5810 6010 6011 6111 6110 6210 6211 6311 6310 6309 6209 6109 6009 5909 5809 5808 5908 6008 6108 6208 6308 6307 6207 6206 6306 6305 6205 6204 6304 6104 6105 6106 6107 6007 5907 5807 5806 5805 5905 5906 6006 6005 6004 6003 6002 6102 6103 6203 6303 6302 6202 6201 6301 6300 6200 6100 6101 6001 6000 5900 5800 5801 5901 5902 5802 5803 5903 5904 5804 5704 5604 5603 5703 5702 5701 5700 5600 5500 5501 5601 5602 5502 5503 5504 5505 5506 5606 5605 5705 5706 5707 5708 5709 5710 5610 5510 5410 5409 5509 5609 5608 5607 5507 5508 5408 5308 5309 5310 5210 5211 5111 5112 5113 5114 5014 5015 4915 4817 4718 4719 4619 4520 4422 4421 4519 4518 4618 4617 4717 4816 4815 4914 5013 4913 4912 5012 5011 4911 4910 4909 5009 5010 5110 5109 5209 5208 5108 5008 5007 5006 5106 5107 5207 5206 5306 5307 5407 5406 5405 5305 5304 5404 5403 5303 5204 5205 5105 5104 5103 5203 5202 5102 5101 5201 5301 5302 5402 5401 5400 5300 5200 5100 5000 5001 5002 5003 5004 5005 4906 4907 4908 4809 4810 4811 4812 4813 4814 4345 4346 4347 4348 6548 6547 6546 4322 4321 4320 4420 4419 4418 4417 4517 4516 4616 9754 9853 9953 4716 4715 4714 4713 4712 4711 4611 4612 4512 4412 4413 4513 4613 4614 4615 4515 4514 4414 4415 4416 4316 4317 4318 4319 4217 4216 4215 4315 4314 4313 4312 4311 4411 4511 4610 4710 4709 4808 4708 4707 4807 4806 4805 4905 4904 4804 4803 4903 4902 4802 4801 4901 4900 4800 4700 4701 4702 4703 4704 4705 4706 4605 4606 4607 4608 4609 4509 4510 4410 4409 4508 4507 4506 4505 4604 4603 4602 4601 4600 4500 4501 4401 4400 4300 4301 4302 4303 4403 4402 4502 4503 4504 4404 4304 4305 4405 4406 4407 4408 4308 4208 4209 4309 4310 4210 4211 4212 4213 4214 4218 4220 4221 4219 4117 4116 4115 4114 4113 4112 4111 4110 4109 4009 4008 4108 4107 4007 4006 4106 4206 4306 4307 4207 4205 4204 4104 4105 4005 4004 3904 3903 4003 4002 4001 4101 4102 4103 4203 4202 4201 4200 4100 4000 3900 3901 3902 3802 3803 3804 3805 3905 3906 3907 3908 3909 3809 3808 3807 3806 3706 3707 3708 3709 3710 3810 3910 4010 4011 3911 3811 3711 3712 3812 3813 3713 3814 3914 3913 3912 4012 4013 4014 4015 4017 4118 4119 4120 4222 4121 4019 4018 4016 3916 3915 3815 3715 3714 3613 3612 3611 3610 3609 3608 3607 3606 3506 3505 3605 3705 3704 3703 3603 3604 3504 3503 3502 3602 3702 3701 3801 3800 3700 3600 3601 3501 3500 3400 3300 3301 3401 3402 3302 3303 3403 3404 3405 3205 3105 3104 3103 3102 3101 3100 3200 3201 3202 3203 3204 3304 3305 3306 3406 3206 3207 3307 3407 3507 3508 3408 3409 3509 3510 3410 3310 3210 3211 3311 3411 3511 3512 3513 3412 3312 3212 3112 3111 3110 3109 3209 3309 3308 3208 3108 3107 3106 3006 3005 3004 3003 3002 3001 2901 2902 2801 2802 2803 2903 2904 2905 2906 3007 3008 3009 3010 3011 2911 2910 2912 3012 3013 3113 3213 3313 3413 3414 3514 3614 3615 3716 3816 3616 3516 3515 3415 3416 3316 3315 3314 3214 3215 3216 3116 3115 3114 3014 3015 2914 2913 2813 2812 2811 2810 2809 2909 2908 2907 2808 2807 2806 2706 2705 2805 2804 2704 2703 2702 2602 2603 2604 2605 2606 2607 2707 2708 2608 2609 2709 2710 2711 2712 2713 2612 2611 2610 2510 2511 2512 2411 2311 2310 2210 2209 2208 2207 2307 2407 2408 2308 2309 2410 2409 2509 2508 2507 2506 2505 2405 2406 2306 2305 2205 2204 2304 2404 2504 2503 2403 2303 2302 2402 2502 2501 2601 2701 3000 2900 2800 2700 2600 2500 2400 2300 2200 2401 2301 2201 2202 2203 2206 2211 2212 2312 2412 2513 2613 2814 2915 2916 3016 3017 3117 3217 3317 3417 3517 3617 3717 3817 3917 3918 3919 3920 4020 4021 4122 4022 3922 3921 3821 3820 3720 3719 3819 3818 3718 3618 3619 3519 3518 3418 3419 3318 3218 3219 3319 3320 3420 3520 3620 3621 3721 3822 3823 3923 4023 4123 4223 4224 4124 4024 3924 3824 3724 3723 3722 3622 3623 3523 3522 3521 3421 3321 3220 3221 3121 3120 3119 3118 3018 2918 2917 2817 2816 2815 2715 2714 2614 2514 2414 2413 2213 2313 2314 2214 2215 2315 2415 2515 2615 2616 2716 2717 2617 2517 2516 2416 2417 2317 2316 2216 2217 2218 2318 2418 2518 2519 2618 2718 2818 2819 2919 3019 3020 2920 2921 3021 3122 3222 3322 3422 3423 3323 3223 3022 2922 2822 2722 2622 2621 2721 2821 2820 2720 2719 2619 2620 2520 2420 2419 2319 2219 2320 2220 2221 2222 2223 2323 2322 2321 2421 2521 2522 2422 2423 2523 2623 2723 2823 2923 3023 3123 3224 3324 3424 3524 3624 3625 3725 3825 3925 4025 4125 4225 4226 4126 4026 3926 3826 3827 3927 4027 4127 4227 4228 4128 4130 4030 4033 4133 4233 4232 4132 4131 4231 4230 4229 4129 4029 4028 3928 3929 3930 3931 4031 4032 3932 3933 3833 3832 3831 3830 3829 3828 3728 3729 3629 3628 3627 3727 3726 3626 3526 3525 3425 3325 3225 3125 3124 3024 2924 3025 2925 2825 2824 2724 2624 2224 2324 2424 2524 2625 2725 2726 2826 2827 2927 2926 3026 3126 3226 3227 3327 3326 3426 3427 3527 3528 3428 3328 3228 3230 3231 3331 3330 3430 3431 3432 3332 3333 3433 3533 3532 3632 3633 3733 3732 3731 3730 3630 3631 3531 3530 3529 3429 3329 3229 3129 3128 3127 3027 3028 2928 2828 2829 2830 2930 2929 3029 3030 3130 3131 3132 3232 3233 3133 3033 3032 3031 2931 2831 2832 2932 2933 2833 2733 2732 2731 2730 2630 2729 2728 2727 2627 2626 2526 2525 2425 2325 2225 2226 2227 2327 2326 2426 2427 2527 2528 2628 2629 2529 2530 2531 2631 2632 2633 2533 2532 2432 2433 2333 2332 2331 2431 2430 2330 2329 2429 2428 2328 2228 2229 2230 2231 2232 3741 3841 3941 3942 4044 4144 4244 4245 4246 4247 4248 4148 4147 4146 4145 4045 4046 4047 3947 4048 3948 3848 3748 3747 3847 3846 3946 3945 3944 3943 4043 4143 4243 4242 4241 4240 4140 4141 4142 4042 4041 4040 3940 3840 3740 3742 3842 3843 3743 3744 3844 3845 3745 3746 3646 3546 3547 3647 3648 3548 3448 3348 3347 3447 3446 3445 3545 3645 3644 3643 3642 3641 3640 3639 3739 3738 3737 3837 3838 3839 4039 3939 3938 3937 4037 4038 4138 4139 4239 4238 4237 4236 4235 4234 4134 4034 3934 3834 3835 3935 4035 4135 4137 4136 4036 3936 3836 3736 3735 3734 3634 3534 3535 3635 3636 3536 3537 3637 3638 3538 3539 3540 3541 3542 3543 3544 3444 3443 3343 3344 3244 3245 3345 3346 3246 3247 3248 3148 3147 3146 3145 3144 3143 3243 3242 3342 3442 3441 3440 3439 3438 3437 3436 3336 3337 3338 3238 3237 3236 3136 3137 3138 3139 3140 3240 3239 3339 3340 3341 3241 3141 3142 3042 3041 3040 3039 3038 3037 3036 3035 3135 3235 3335 3435 3434 3334 3234 3134 3034 2934 2935 2936 2937 2938 2838 2837 2738 2839 2939 2940 2941 2942 2842 2843 2844 2845 2846 2946 2945 2944 2943 3043 3044 3045 3046 3047 3048 2948 2947 2847 2848 2748 2747 2746 2745 2744 2743 2742 2741 2841 2840 2740 2739 2639 2638 2737 2637 2636 2736 2836 2835 2834 2734 2735 2635 2634 2534 2434 2334 2234 2134 2135 2235 2035 2034 1934 2233 1834 1835 1935 1936 2036 2136 2236 2237 2137 2138 2238 2338 2337 2437 2436 2336 2335 2435 2535 2536 2537 2538 2438 2439 2539 2540 2640 2641 2541 2542 2642 2643 2644 2645 2646 2647 2648 2548 2547 2447 2546 2545 2544 2543 2443 2442 2342 2341 2441 2440 2340 2339 2239 2139 2039 2038 2037 1937 1938 1939 1940 1840 2040 2140 2240 2241 2242 2243 2343 2444 2445 2446 6646 6647 6648 9854 9954 2448 2348 2347 2346 2246 2245 2345 2344 2244 2144 2143 2142 2141 2041 1941 1841 1839 1838 1837 1836 1736 1735 1734 1733 1833 1933 2033 2133 2132 2032 1932 1832 1831 1931 1930 1929 1928 1828 1728 1729 1730 1830 1829 2029 2030 2031 2131 2130 2129 2128 2028 2027 2127 2126 2026 2025 2125 2124 2024 1924 1824 1724 1725 1726 1826 1825 1925 1926 1927 1827 1727 1627 1628 1629 1630 1631 1731 1732 1632 1633 1634 1635 1636 1637 1737 1738 1739 1740 1741 1742 1842 1942 2042 2043 2044 1944 1943 1843 1743 1844 1744 1644 1645 1745 1845 1945 2045 2145 2146 2247 2248 2147 2046 1946 1846 1746 1646 1643 1642 1641 1640 1639 1638 1626 1625 1624 1623 1723 1823 1923 1922 1822 1820 1920 2020 2120 2121 2122 2123 2023 2022 2021 1921 1821 1721 1722 1622 1621 1620 1619 1618 1718 1719 1720 1819 1919 2019 2119 2118 2018 1918 1818 1917 1817 1717 1617 1616 1716 1816 1916 2016 2017 2117 2116 2115 2015 1915 1815 1814 1914 2014 2114 2113 2013 2012 2112 2111 2110 2109 2108 2107 2106 2105 2005 2004 2104 2103 2102 2101 2001 1901 1902 2002 2003 1903 1904 1804 1805 1905 1906 2006 1907 2007 2008 2009 2010 2011 1911 1912 1913 1813 1812 1811 1810 1809 1909 1910 1908 1808 1807 1806 1706 1705 1704 1703 1803 1802 1801 1701 1601 1702 1602 1603 1604 1605 1606 1607 1707 1708 1709 1710 1711 1712 1713 1714 1715 1615 1614 1613 1612 1611 1610 1609 1608 1507 1506 1505 1504 1503 1502 1501 1401 1301 1201 1101 1001 901 2100 2000 1900 1800 1700 1600 1500 1400 1300 1200 1100 1000 900 800 700 701 801 802 702 703 704 804 803 903 902 1002 1102 1202 1203 1204 1304 1303 1302 1402 1403 1404 1405 1406 1407 1408 1508 1308 1307 1306 1305 1205 1206 1106 1006 1005 1105 1104 1103 1003 1004 904 905 906 806 805 705 706 707 807 907 1007 1107 1207 1208 1108 1008 1009 1109 1209 1309 1310 1210 1211 1311 1411 1410 1409 1509 1510 1511 1512 1513 1514 1515 1413 1412 1312 1212 1112 1111 1110 1010 1011 1012 912 911 910 909 908 808 809 709 710 810 811 711 611 610 609 708 608 607 508 507 506 606 605 604 603 602 502 503 403 402 401 501 601 600 500 400 300 200 100 0 1 101 201 301 302 303 203 202 102 2 3 103 104 204 304 404 504 505 405 406 407 408 308 307 306 305 205 105 4 5 6 7 8 108 107 106 206 207 208 209 210 310 309 409 509 510 511 410 411 311 211 111 110 109 9 10 11 12 13 113 112 212 213 313 312 412 413 513 512 612 712 812 813 913 1013 1113 1114 1014 914 814 713 613 614 714 715 815 915 1015 1115 1215 1315 1313 1213 1214 1314 1414 1415 1647 1747 1947 2047 2148 1847 1516 1416 1316 1216 1116 1016 916 917 1017 1117 1417 1517 1518 1519 1520 1420 1421 1521 1321 1320 1319 1419 1418 1318 1317 1217 1218 1219 1220 1221 1121 1120 1020 1019 1119 1118 1018 918 817 816 716 717 617 616 615 515 514 414 314 214 215 115 114 14 15 16 17 18 19 119 118 117 116 216 217 218 219 319 419 418 318 317 316 315 415 516 416 417 517 518 519 619 618 718 818 819 719 720 820 919 920 921 1021 1022 1122 1222 1322 1422 1522 1523 1423 1323 1324 1224 1223 1123 922 822 821 721 621 620 521 520 420 320 220 120 20 21 121 221 222 122 22 23 123 223 224 124 24 25 125 126 26 27 127 227 228 128 328 327 326 226 225 325 324 323 322 321 421 422 423 523 522 722 622 623 723 823 824 924 923 1023 1024 1124 1025 1125 1225 1325 1326 1327 1427 1426 1425 1424 1524 1525 1526 1527 1528 1529 1429 1428 1328 1228 1128 1127 1227 1226 1126 1026 926 925 825 826 726 626 625 725 724 624 524 424 425 525 526 426 427 527 627 628 728 727 827 927 1027 1028 928 828 829 729 730 830 930 929 1029 1129 1130 1030 1031 1131 1231 1230 1229 1329 1330 1430 1530 1531 1532 1432 1431 1331 1332 1232 1132 1032 932 931 831 832 732 731 631 630 629 529 528 428 429 430 530 531 431 432 532 632 332 232 231 331 330 329 229 230 130 129 28 29 30 31 131 132 32 33 133 233 333 433 533 534 634 633 733 734 834 833 933 934 1034 1035 1033 1133 1134 1135 1235 1234 1233 1333 1433 1533 1534 1535 1536 1537 1538 1438 1338 1337 1437 1436 1435 1434 1334 1335 1336 1236 1237 1238 1138 1137 1136 1036 935 936 836 835 735 736 636 635 535 536 436 336 335 435 434 334 234 134 34 35 135 235 236 136 36 37 38 138 137 237 238 338 337 437 438 538 537 637 638 738 737 837 838 938 937 1037 1038 1039 1139 1239 1339 1340 1240 1140 1141 1241 1341 1441 1440 1439 1539 1540 1541 1542 1543 1443 1442 1342 1343 1243 1242 1142 1143 1244 1344 1444 1544 1545 1445 1446 1447 1347 1346 1546 1547 1548 1448 1449 1549 1550 1450 1350 1349 1348 1248 1148 1149 1249 1250 1049 1048 1047 1147 1247 1246 1345 1245 1146 1046 1045 1145 1144 1044 1043 1042 1041 1040 939 839 739 639 539 540 440 439 339 239 139 39 40 140 141 241 240 340 341 441 541 641 640 740 741 841 840 940 941 942 943 944 844 843 842 742 642 542 442 342 242 142 41 42 43 143 243 244 144 44 45 145 245 345 445 444 344 343 443 543 643 743 744 745 746 747 748 648 647 646 645 644 544 545 546 446 346 246 247 147 146 46 47 48 148 248 348 347 447 547 548 448 349 249 149 49 50 150 250 350 352 452 451 351 251 252 152 151 51 52 53 153 253 353 453 553 552 551 550 450 449 549 649 749 849 848 847 846 845 1050 1150 1648 1948 2048 6747 6746 6748 1848 1748 1551 1451 1351 1251 1151 1051 945 946 947 948 949 950 850 750 650 651 652 653 753 752 751 851 951 952 852 853 953 954 854 855 955 956 856 756 755 754 654 554 454 354 254 255 155 154 54 55 56 156 256 356 355 455 456 556 555 655 656 657 557 558 457 458 358 357 257 157 57 58 158 258 259 359 459 559 560 660 760 759 659 658 758 757 857 957 958 858 859 959 960 860 861 961 962 862 762 761 661 662 562 561 461 460 360 361 260 160 159 59 60 61 62 63 64 65 165 164 163 162 161 261 262 362 462 463 464 364 363 263 264 265 365 465 565 665 664 564 563 663 763 863 963 964 864 764 765 865 965 966 866 766 666 566 466 366 266 166 66 67 167 168 68 69 169 269 369 368 268 267 367 467 468 568 567 667 668 768 767 867 967 968 868 769 669 869 969 970 971 972 973 974 874 873 773 772 872 871 870 770 771 670 570 569 469 470 370 270 170 70 71 171 271 371 372 272 273 373 374 473 472 471 571 671 672 572 573 673 674 774 775 875 975 976 876 776 675 676 576 575 574 474 475 476 376 375 275 274 173 172 72 73 74 174 175 75 76 176 276 277 377 477 577 677 777 877 977 978 878 778 678 578 478 378 278 178 177 77 78 79 80 81 82 182 181 180 179 279 280 281 381 380 379 479 480 481 482 382 282 283 183 83 84 184 284 384 383 483 484 584 583 683 783 782 682 582 581 580 579 679 680 681 781 780 779 879 979 980 880 881 882 982 981 983 883 784 684 685 585 485 385 386 286 285 185 85 86 87 186 187 287 387 487 486 586 686 786 785 885 886 884 984 985 1085 1084 1284 1384 1484 1584 1583 1483 1482 1582 1581 1580 1579 1479 1379 1279 1280 1380 1480 1481 1381 1281 1181 1180 1179 1079 1080 1081 1082 1083 1283 1383 1382 1282 1182 1183 1184 1185 1186 1286 1285 1385 1386 1486 1485 1585 1586 1587 1588 1589 1489 1488 1487 1387 1287 1187 1087 1086 986 987 887 787 587 687 688 788 888 988 1088 1188 1288 1388 1389 1289 1290 1291 1391 1390 1490 1491 1590 1591 1592 1593 1594 1595 1495 1494 1493 1492 1392 1393 1293 1292 1192 1191 1090 1190 1189 1089 989 990 890 889 789 790 791 891 991 1091 1092 1193 1093 1094 994 993 992 892 792 793 893 894 895 995 996 1096 1095 1195 1295 1296 1297 1397 1497 1498 1398 1399 1499 1599 1598 1597 1596 1496 1396 1395 1394 1294 1194 1196 1197 1097 1098 1198 1298 1299 1199 1099 999 998 997 897 797 896 796 795 794 694 695 696 697 698 798 898 899 799 699 599 499 598 597 596 595 594 593 693 692 691 690 689 588 589 590 591 592 492 493 494 495 496 396 296 196 96 97 197 297 298 198 98 99 199 299 399 398 498 497 397 395 295 195 95 94 194 294 394 393 293 292 392 491 490 489 488 1252 1352 1452 1552 3090 2990 2890 2889 2989 3089 3088 3188 3189 3190 1152 1052 288 188 88 89 90 91 92 93 193 192 191 291 391 390 290 190 189 289 389 388 1649 1749 1849 1949 2049 2149 3290 3289 3288 3287 3187 3087 3186 3086 2986 2987 2988 2888 2887 2787 2788 2688 2689 2789 2790 2690 2590 2589 2588 2587 2687 2686 2586 2585 2685 2785 2786 2886 2885 2985 3085 3185 3285 3286 3386 3385 3485 3585 3685 3686 3687 3688 3588 3587 3586 3486 3487 3387 3388 3488 3489 3389 3390 3490 3590 3589 3689 3690 3691 3591 3491 3391 3291 3191 3392 3492 3493 3393 3394 3494 3594 3593 3592 3692 3693 3694 3695 3696 3697 3597 3596 3595 3495 3395 3496 3497 3498 3598 3698 3699 3599 3499 3399 3398 3298 3299 3199 3099 2999 2998 3098 3198 3197 3297 3397 3396 3296 3196 3195 3295 3294 3293 3292 3192 3193 3093 2993 2992 3092 3091 2991 2891 2892 2893 2894 2895 2995 2994 3194 3094 3095 3096 3097 2997 2996 2896 2897 2898 2899 2799 2699 2698 2798 2797 2796 2696 2596 2496 2396 2395 2495 2595 2594 2593 2692 2691 2791 2792 2793 2693 2694 2794 2795 2695 2697 2597 2598 2599 2499 2498 2497 2397 2398 2399 2299 2298 2198 2199 2099 1999 1899 1799 1699 1698 1697 1696 1796 1797 1798 1898 1897 1997 1998 2098 2097 2197 2297 2296 2295 2294 2494 2394 2393 2493 2492 2592 2591 2491 2391 2392 2292 2293 2193 2194 2195 2196 2096 2095 2094 1994 1995 1996 1896 1895 1894 1794 1795 1695 1694 1693 1793 1893 1993 2093 2092 2192 2291 2191 2091 2090 2190 2189 2089 1989 1889 1890 1790 1789 1689 1690 1691 1692 1792 1791 1891 1892 1992 1991 1990 2088 1988 1888 1887 1787 1788 1688 1687 1686 1786 1886 1986 1987 2087 2187 2188 2288 2287 2387 2388 2389 2289 2290 2390 2490 2489 2488 2487 2486 2485 2385 2386 2286 2285 2185 2186 2086 2085 1985 1885 1884 1984 1983 1982 1981 1980 2080 2180 2280 2380 6848 6846 6847 1750 1650 1850 1950 2178 2278 2378 2379 2279 2179 2079 1979 1879 1880 1881 1882 1883 1782 1783 1784 1785 1685 1684 1683 1682 1681 1680 1679 1779 1780 1781 2081 2082 2083 2084 2184 2284 2283 2282 2281 2181 2182 2183 2383 2384 2484 2483 2482 2382 2381 2481 2480 2479 2478 2477 2377 2277 2177 2077 2078 1978 1878 1778 1678 1677 1676 1675 1674 1774 1775 1776 1777 1877 1977 1976 1876 1875 1975 2075 2076 2176 2276 2376 2476 2475 2375 2275 2175 2174 2274 2374 2474 2473 2472 2372 2373 2273 2272 2173 2172 2072 2073 2074 1874 1974 1973 1972 1872 1873 1773 1673 1574 1575 1576 1476 1475 1474 1374 1375 1376 1377 1477 1577 1578 1478 1378 1278 1178 1078 1077 1177 1277 1276 1176 1076 1075 1175 1275 1274 1273 1173 1174 1074 1073 1072 1071 1171 1172 1272 1271 1371 1372 1373 1473 1573 1572 1472 1471 1469 1369 1368 1367 1267 1268 1168 1167 1067 1068 1069 1070 1170 1169 1269 1270 1370 1470 1571 1570 1569 1568 1468 1467 1567 1667 1668 1669 1769 1770 1670 1671 1672 1772 1771 1871 1971 2071 2371 2471 2271 2171 1970 1870 1869 1868 1768 1767 1867 1951 2050 2150 2249 2250 2051 1851 1751 1651 1560 1559 1558 1557 1556 1555 1554 1553 1453 1353 1253 1153 1053 1054 1055 1056 1156 1155 1154 1254 1255 1355 1354 1454 1455 1456 1457 1357 1356 1256 1257 1157 1057 1058 1158 1258 1358 1458 1459 1359 1259 1159 1059 1060 1061 1062 1162 1163 1063 1064 1065 1066 1166 1266 1265 1165 1164 1264 1263 1262 1261 1161 1160 1260 1460 1360 1361 1461 1561 1562 1563 1463 1462 1362 1363 1364 1464 1564 1565 1465 1365 1366 1466 1566 1666 1766 1866 1865 1765 1665 1664 1764 1864 1964 1965 2065 2066 1966 1967 2067 2068 1968 1969 2069 2070 2170 2270 2370 2470 2469 2369 2269 2169 2168 2268 2267 2167 2166 2165 2164 2064 2063 1963 1863 1763 1663 1662 1661 1660 1659 1658 1657 1656 1655 1654 1653 1652 1752 1753 1852 1952 1953 1853 1854 1754 1755 1855 1856 1756 1757 1758 1858 1857 1957 1956 1955 1954 2053 2052 2151 2251 2349 2350 9955 9855 2363 2364 2365 2367 2368 2366 2266 2265 2264 2263 2163 2162 2062 1962 1862 1762 1761 1760 1759 1859 1959 1960 1860 1861 1961 2061 2161 2262 2362 2361 2261 2260 2160 2060 2059 1958 2058 2057 2056 2055 2054 2154 2153 2152 2252 2253 2254 2255 2155 2156 2157 2158 2159 2259 2258 2257 2256 2356 2355 2354 2353 2352 2351 2451 2450 2449 2549 2550 2551 2553 2552 2452 2453 2454 2455 2555 2554 2654 2655 2656 2456 2556 2557 2457 2357 2358 2458 2558 2559 2560 2460 2360 2359 2459 2461 2462 2468 2467 2466 2465 2464 2463 2562 2561 2661 2660 2659 2658 2657 2757 2756 2755 2754 2753 2653 2652 2651 2649 2650 2751 2752 2852 2952 3052 3053 2953 2853 2854 2954 3054 3154 3254 3253 3153 3152 3352 3252 3251 3151 3051 3050 2950 2951 2851 2850 2750 2749 2849 2949 3049 3149 3150 3250 3249 3349 3350 3351 3451 3452 3453 3353 3354 3454 3553 3552 3652 3752 3751 3750 3749 3649 3549 3449 3450 3550 3551 3650 3651 3851 3850 3849 3949 4049 4149 4150 4151 4152 4052 4051 4050 3950 3951 3952 3852 3853 3653 3753 3754 3854 3954 3953 4053 4153 4253 4252 4251 4351 4350 4250 4249 4349 4449 4549 4550 4551 4552 4553 4554 4654 4754 4854 4853 4852 4752 4753 4653 4652 4651 4751 4851 4750 4749 4649 4650 4450 4451 4452 4352 4353 4453 4454 4354 4254 4154 4054 3654 3554 2855 2856 2857 2858 2758 2759 2760 2761 2662 2762 2763 2663 2563 2564 2664 2665 2565 2566 2567 2568 2668 2768 2767 2667 2666 2766 2765 2764 2864 2863 2862 2861 2860 2859 2959 2960 2961 2962 2963 2964 3064 3063 3163 3162 3062 3061 3161 3160 3060 3059 3159 3158 3058 2958 2957 3057 3157 3257 3256 3156 3056 2956 2955 3055 3155 3255 3355 3356 3357 3358 3258 3259 3359 3459 3458 3558 3559 3560 3460 3360 3260 3261 3262 3263 3264 3164 3165 3065 2965 2865 2866 2966 3066 3166 3167 3067 2967 2867 2868 2669 2569 2769 2869 2969 2968 3068 3069 3169 3168 3268 3267 3266 3265 3365 3366 3466 3465 3464 3364 3363 3463 3462 3362 3361 3461 3561 3661 3761 6947 6946 6948 3861 3660 3659 3658 3657 3557 3457 3456 3455 3555 3556 3656 3655 3755 3756 3757 3758 3759 3760 3762 3662 3562 3563 3564 3565 3566 3567 3467 3367 3368 3369 3269 3170 3070 2970 2870 2770 2771 2871 2872 2772 2672 2671 2670 2570 2571 2572 2573 2673 2674 2574 2575 2675 2775 2875 2874 2774 2773 2873 2973 3073 3072 2972 2971 3071 3171 3172 3270 3271 3371 3370 3469 3468 3568 3668 3667 3767 3766 3666 3665 3765 3764 3664 3663 3763 3864 3863 3862 3860 3859 3858 3857 3856 3855 3955 3956 3957 3958 3959 3960 3961 3962 3963 3964 3965 3865 3866 3867 3868 3768 3769 3669 3569 3470 3471 3472 3372 3272 3273 3173 3174 3074 2974 2975 2976 2977 2877 2876 2776 2676 2576 2577 2677 2777 2778 2678 2578 2579 2679 2680 2580 2581 2681 2781 2780 2779 2880 2879 2878 2978 3078 3077 3076 3075 3175 3275 3274 3374 3373 3473 3474 3475 3375 3476 3376 3276 3176 3177 3178 3179 3079 2979 2980 2981 2881 2782 2682 2582 2583 2584 2684 2683 2783 2784 2884 2883 2882 2982 3082 3083 2983 2984 3084 3184 3183 3182 3181 3081 3080 3180 3280 3279 3278 3277 3377 3378 3379 3380 3381 3281 3282 3283 3284 3384 3383 3382 3482 3481 3681 3682 3683 3684 3584 3484 3483 3583 3582 3581 3480 3479 3478 3477 3577 3677 3576 3575 3574 3573 3572 3571 3570 3670 3671 3771 3770 3870 3869 3966 3967 3968 3969 3970 3871 3872 3772 3672 3673 3674 3675 3676 3776 3775 3875 3975 3974 3973 3873 3773 3774 3874 3876 3877 3777 3778 3678 3578 3579 3580 3680 3679 3779 3879 3878 3978 3979 4079 4080 3980 3880 3780 3781 3782 3882 3881 3981 4081 4082 4083 4183 4283 4284 4184 4084 3984 3884 3784 3783 3883 3983 3982 4182 4282 4281 4181 4180 4280 4179 4178 4078 4077 3977 3976 4076 4075 4074 4073 3972 3971 4060 4059 4058 4057 4056 4850 4849 4055 4061 4062 4063 4064 4065 4066 4067 4068 4069 4070 4071 4072 4173 4174 4175 4176 4177 4277 4276 4376 4377 4378 4278 4279 4379 4380 4381 4382 4482 4582 4583 4483 4383 4384 4484 4584 4684 4683 4682 4681 4581 4481 4480 4479 4579 4679 4678 4778 4777 4677 4676 4776 4876 4877 4878 4879 4779 4780 4680 4580 4578 4478 4477 4577 4576 4476 4475 4375 4275 4274 4374 4273 4172 4171 4272 4373 4473 4474 4574 4575 4675 4674 4774 4775 4875 4975 4976 5076 5077 4977 4979 4978 5078 5079 5080 4980 4880 4882 4883 4884 4784 4783 4782 4781 4881 4981 4982 4983 4984 4985 4988 5088 5089 4989 4990 4991 4992 4993 4994 4995 5095 5096 4996 4997 4998 4999 5099 5199 5198 5098 5097 5197 5196 5195 5194 5094 5093 5092 5192 5193 5191 5091 5090 5190 5189 5188 5187 5087 4987 4986 5086 5186 5185 5085 5084 5184 5183 5083 5081 5082 5182 5181 5180 5179 5178 5177 5176 5075 5175 5174 5074 4974 4874 4773 4673 4573 4472 4372 4271 4170 4160 4159 4157 4155 4156 4158 4161 4162 4163 4164 4165 4166 4167 4168 4169 4270 4370 4371 4572 4672 4772 4873 5073 5173 4973 4885 4785 4685 4585 4485 4486 4586 4686 4786 4886 4887 4888 4889 4890 4790 4690 4589 4588 4688 4689 4789 4788 4787 4687 4587 4487 4488 4489 4389 4388 4387 4287 4286 4386 4385 4285 4185 4186 4187 4087 4086 4085 3985 3885 3785 3786 3787 3788 3888 3887 3886 3986 3987 3988 4088 4089 4189 4188 4288 4289 4290 4390 4490 4590 4591 4491 4391 4291 4292 4392 4192 4092 4091 4191 4190 4090 3990 3989 3789 3889 3890 3790 3791 3792 3793 3794 3894 3994 3993 3992 3991 3891 3892 3893 4093 4193 4293 4393 4493 4492 4592 4691 4791 4792 4692 4593 4494 4394 4395 4295 4294 4194 4094 4095 4195 4196 4096 4097 3997 3897 3896 3996 3995 3895 3795 3796 3797 3798 3898 3899 3799 3999 3998 4098 4099 4199 4198 4197 4297 4296 4396 4397 4398 4298 4299 4399 4499 4599 4598 4498 4497 4496 4495 4596 4595 4594 4694 4693 4793 4794 4796 4896 4897 4797 4798 4898 4899 4799 4699 4698 4597 4697 4696 4695 4795 4895 4894 4893 4892 4891 4872 4972 5072 4771 4671 4571 4471 4470 4369 4269 4268 4267 4266 4265 4264 4263 4262 4261 4260 4259 4258 4257 4256 4255 4355 4356 4357 4358 4359 4360 4361 4362 4363 4364 4365 4366 4367 4368 4469 4570 4670 4770 4871 4971 5071 5172 5171 5170 5070 4970 4870 4869 4769 4669 4569 4568 4468 4467 4567 4566 4466 4465 4565 4564 4464 4463 4462 4563 4663 4763 4764 4664 4665 4765 4865 4866 4766 4666 4667 4668 4768 4868 4867 4767 4967 4966 4965 5065 5066 5067 5068 4968 4969 5069 5169 5168 5167 5166 5165 5164 5064 4964 4864 4863 4963 4962 4862 4762 4662 4562 4561 4461 4460 4560 4559 4459 4458 4457 4456 4455 4555 4556 4557 4657 4757 4756 4656 4655 4755 4855 4856 4857 4858 4859 4860 4760 4759 4758 4558 4658 4659 4660 4661 4761 4861 4961 4960 4959 4958 4957 5057 5056 4956 4955 5055 5155 5255 5256 5156 5157 5158 5058 5059 5159 5160 5060 5061 5062 5063 5163 5263 5262 5162 5161 5261 5362 5361 5360 5260 5259 5359 5358 5258 5257 5357 5457 5458 5459 5460 5560 5559 5558 5557 5556 5456 5356 5355 5455 5555 5655 5656 5657 5757 5857 5856 5756 5755 5855 5955 6055 6155 6255 7046 7047 7048 6355 6356 6256 6156 6056 5956 5957 6057 6157 6257 6258 6158 6159 6058 5958 5858 5859 5759 5758 5658 5659 5660 5661 5662 5562 5561 5461 5462 5463 5363 5364 5264 5265 5365 5465 5464 5564 5563 5663 5664 5764 5763 5762 5761 5760 5860 5960 5959 6059 6060 6061 5961 5861 5862 5863 5864 5964 5965 5963 5962 6062 6063 6163 6162 6161 6160 6259 6260 6360 6359 6358 6357 6457 6456 6455 4949 4950 6555 6556 6557 6558 6458 6459 6460 6461 6361 6261 6262 6362 6363 6263 6264 6164 6064 6065 6066 5966 5866 5865 5765 5665 5565 5566 5567 5568 5768 5668 5667 5666 5766 5767 5867 5868 5968 5967 6067 6068 6168 6167 6166 6165 6265 6364 6365 6366 6266 6267 6268 6269 6169 6069 5969 5869 5769 5669 5569 5570 5571 5572 5672 5772 5771 5671 5670 5770 5870 5970 6070 6270 6170 6171 6071 5971 5871 5872 5972 6072 6172 6272 6271 6371 6370 6369 9956 9856 9755 6470 6469 6468 6368 6367 6467 6466 6464 6465 6565 6564 6563 6463 6462 6562 6561 6560 6559 6656 6655 6657 6658 6659 6660 6661 6662 6663 6664 6665 6666 6566 6567 6568 6569 6570 6571 6471 6472 6372 6373 6273 6173 6073 5973 5873 5773 5673 5573 5574 5474 5473 5472 5471 5470 5469 5468 5467 5466 5366 5266 5267 5367 5368 5268 5269 5369 5370 5270 5271 5371 5372 5272 5273 5373 5374 5274 5275 5375 5475 5575 5675 5674 5774 5775 5875 5874 5974 6074 6174 6374 6274 6275 6375 6475 6474 6473 6573 6572 6667 6668 6669 6670 6671 6672 6673 6674 6574 6575 6576 6476 6477 6478 6378 6377 6376 6276 6277 6177 6176 6175 6075 5975 5976 6076 6077 5977 5877 5876 5776 5676 5576 5577 5677 5777 5778 5678 5578 5478 5477 5476 5376 5276 5277 5377 5378 5278 5279 5379 5479 5579 5580 5480 5481 5581 5681 5680 5679 5878 5978 6078 6178 6278 6578 6577 6676 6675 6775 6774 6773 6772 6771 6770 6769 6768 6767 6766 6765 6764 6763 6762 6761 6760 6759 6755 6756 6757 6758 6861 6862 6863 6864 6865 6866 6966 6967 6867 6868 6968 6969 6869 6870 6871 6971 6970 7070 7071 7072 6972 6872 6873 6973 6974 6874 6875 6975 6976 6876 6776 6777 6677 6678 6778 6878 6877 6977 6978 7078 7178 7177 7077 7075 7076 7176 7175 7174 7074 7073 7173 7172 7171 7170 7169 7069 7068 7067 7066 7065 6965 6964 6963 6962 6961 6860 6960 6959 6859 6858 6857 6856 6855 5554 5454 5453 5353 5354 5254 5253 5252 5251 5150 5250 5249 5149 5049 5050 5051 4951 4952 4953 4954 5054 5154 5153 5053 5052 5152 5151 5351 5352 5452 5451 5450 5350 5349 5449 5549 5550 5551 5651 5652 5552 5553 5653 5654 5753 5752 5751 5750 5650 5649 5749 5849 5949 6049 6149 6249 7049 7146 7147 7148 7149 6955 6956 6957 6958 7058 7059 7060 7061 7062 7063 7064 7168 7275 7276 7277 7278 5779 5780 5781 5380 5280 7274 7273 7272 7271 7270 7269 7268 7167 7166 7165 7164 7163 7162 7161 7160 7159 7158 7157 7057 7056 7055 7054 6954 6854 6754 6654 6554 6454 6354 6254 6252 6152 6151 6251 6250 6150 6050 5950 5850 5851 5852 5853 5754 5854 5954 5953 5952 5951 6051 6052 6053 6054 6154 6153 6253 6353 6352 6452 6453 6553 6552 6652 6653 6753 6752 6852 6853 6953 6952 6951 6851 6751 6750 6650 6651 6551 6451 6351 6350 6349 6449 6450 6550 6549 6649 6749 6849 6949 6950 6850 7050 7051 7151 7150 7246 7247 7248 7249 7250 7251 7152 7052 7053 7153 7154 7155 7156 7256 7257 7258 7259 7260 7261 7262 7263 7264 7265 7266 7267 7368 7369 7370 7371 7372 7373 7374 7375 7378 7377 7376 7367 7366 7365 7364 7363 7463 7462 7362 7361 7461 7460 7360 7359 7358 7458 7459 7559 7558 7557 7556 7456 7457 7357 7356 7355 7255 7254 7253 7252 7352 7353 7354 7454 7455 7555 7554 7654 7655 7656 7657 7658 7659 7660 7560 7561 7562 7563 7564 7464 7465 7466 7467 7468 7567 7566 7565 7664 7663 7662 7661 7761 7760 7759 7758 7757 7756 7755 7754 7753 7653 7553 7453 7452 7451 7351 7350 7450 7449 7349 7348 7347 7346 7446 7447 7448 7548 7549 7550 7551 7552 7652 7752 7751 7651 7650 7750 7749 7649 7648 7647 7547 7546 7646 7746 7846 7847 7747 7748 7848 7849 7850 7852 7851 7951 7952 7953 7853 7854 7855 7856 7857 7858 7859 7860 7960 7961 7861 7862 7762 7763 7764 7765 7665 7666 7667 7568 7469 7470 7471 7472 7473 7474 7475 5381 5281 5881 5880 5879 7767 7766 7866 7865 7864 7863 7963 7962 8061 8060 8059 7959 7958 7957 7956 7955 7954 8054 8053 8052 8051 8050 7950 7949 7948 7947 7946 8046 8047 8048 8049 8149 8150 8151 8152 8153 8154 8155 8055 8056 8156 8157 8057 8058 8158 8159 8160 8161 8163 8263 9655 9756 9957 9857 7968 7868 7867 7967 7966 7965 7964 8064 8063 8062 8162 8262 8261 8260 8259 8258 8257 8256 8255 8254 8253 8252 8251 8250 8249 8248 8148 8147 8146 8246 8247 8347 8348 8349 8350 8351 8352 8353 8354 8355 8455 8456 8356 8357 8358 8359 8360 8361 8362 8363 8364 8264 8164 8065 8066 8067 7768 7668 7569 7570 7571 7572 7476 7477 7478 7575 7574 7573 7669 7769 7869 7969 8069 8068 8166 8165 8265 8365 8465 8464 8463 8462 8461 8460 8459 8458 8457 8558 8557 8556 8555 8655 8656 8657 8658 8659 8559 8560 8561 8562 8563 8564 8565 8665 8666 8566 8466 8366 8266 8267 8167 8168 8268 8367 8467 8567 8667 8767 8766 8765 8764 8664 8663 8763 8762 8662 8661 8761 8660 8760 8759 8758 8757 8756 8755 8754 8654 8554 8454 8453 8553 8552 8452 8451 8551 8550 8450 8449 8448 8447 8346 8446 8546 8547 8647 8646 8648 8548 8549 8649 8650 8651 8652 8653 8753 8752 8751 8750 8850 8849 8749 8748 8747 8746 8846 8946 9046 9146 9147 9247 9246 9346 9347 9348 9248 9148 9149 9249 9349 9350 9250 9251 9351 9352 9252 9253 9153 9152 9052 9051 9151 9150 9050 9049 9048 9047 8947 8847 8848 8948 8949 8950 8851 8951 8952 8852 8853 8953 9053 9054 9154 9254 9353 9354 9355 9255 9256 9356 9357 9257 9157 9156 9155 9055 8955 8954 8854 8855 8857 8856 8956 9056 9057 8957 8958 8858 8859 8860 8960 8959 9059 9058 9158 9159 9259 9258 9358 9359 9360 9260 9160 9060 9061 8961 8861 8862 8863 8864 8865 8768 8668 8568 8468 8368 8169 7870 7770 7670 7671 7672 7673 7674 7675 7576 7577 7578 7774 7773 7772 7771 7871 7971 7970 8070 8269 8369 8469 8569 8669 8769 8866 8965 8964 8963 8962 9062 9162 9161 9361 9261 9262 9362 9462 9461 9458 9457 9456 9455 9555 9556 9656 9657 9757 9758 9858 9958 9959 9960 9961 9861 9860 9859 9759 9760 9660 9659 9658 9557 9558 9559 9459 9460 9560 9561 9661 9761 9762 9662 9562 9563 9463 9363 9263 9163 9063 9064 9065 9066 9166 9165 9164 9264 9265 9365 9364 9464 9564 9664 9663 9763 9863 9862 9962 9963 9964 9965 9865 9864 9764 9765 9665 9666 9566 9565 9465 9466 9366 9266 9267 9167 9067 8966 8967 8867 8968 9068 9168 9268 9368 9367 9467 9468 9469 9569 9568 9567 9667 9767 9766 9866 9966 9967 9867 9868 9968 9768 9668 9669 9769 9869 9969 9970 9870 9770 9670 9570 9470 9370 9369 9269 9270 9170 9169 9069 9070 8970 8969 8869 8868 8870 8770 8670 8570 8470 8370 8270 8170 8171 8271 8272 8173 8172 8071 8072 7972 7872 7873 7973 8073 8074 7974 7874 7875 7775 7776 7676 7677 7678 7778 7777 7877 7876 7976 7975 8075 8175 8174 8273 8373 8374 8274 8275 8375 8475 8474 8574 8573 8473 8472 8372 8371 8471 8571 8572 8672 8673 8671 8771 8871 8971 9071 9072 9073 9173 9172 9171 9271 9371 9471 9571 9671 9771 9871 9971 9972 9872 9973 9873 9773 9772 9672 9673 9573 9572 9472 9473 9373 9372 9272 9273 9274 9174 9074 8974 8973 8972 8872 8772 8773 8873 8874 8774 8674 8675 8575 8576 8476 8376 8276 8176 8076 7977 7878 7978 8078 8077 8177 8277 8377 8477 8577 8677 8676 8776 8775 8875 8975 9075 9175 9275 9375 9374 9474 9574 9674 9774 9874 9974 9975 9875 9775 9675 9575 9475 9476 9376 9276 9277 9177 9176 9076 9077 8977 8976 8876 8877 8777 8778 8678 8578 8478 8378 8379 8279 8278 8178 8179 8079 7979 7879 7779 7679 7579 5979 5980 5981 5282 5382 7680 7780 7880 7881 7981 7980 8080 8081 8181 8180 8280 8380 8480 8479 8579 8679 8779 8879 8878 8978 9078 8979 9079 9179 9178 9278 9378 9377 9477 9478 9578 9577 9576 9676 9776 9876 9976 9977 9877 9777 9677 9678 9579 9479 9480 9380 9379 9279 9280 9180 9080 8980 8880 8780 8680 8580 8581 8481 8482 8582 8682 8683 8681 8781 8782 8882 8982 8981 8881 9081 9082 9083 8983 8883 8783 8784 8684 8584 8583 8483 8383 8382 8381 8281 8282 8182 8082 8083 7983 7982 7882 7883 7783 7782 7781 7681 7682 7683 7583 7582 7581 7580 7479 7480 7481 7482 7483 7484 7584 7684 7784 7884 7984 8084 8184 8183 8283 8284 8384 8484 8884 8984 9084 9184 9183 9182 9181 9281 9282 9382 9381 9481 9581 9580 9680 9681 9781 9881 9880 9780 9679 9779 9778 9978 9878 9879 9979 9980 9981 9982 9882 9782 9783 9883 9983 9984 9985 9986 9886 9885 9884 9784 9785 9786 9686 9685 9684 9584 9583 9683 9682 9582 9482 9483 9383 9283 9284 9384 9484 9485 9585 9586 9486 9386 9385 9285 9286 9287 9387 9487 9587 9588 9688 9687 9787 9788 9888 9887 9987 9988 9989 9889 9789 9790 9890 9990 9991 9891 9791 9792 9892 9992 9993 9893 9994 9995 9996 9997 9998 9999 9899 9799 9699 9698 9798 9898 9897 9797 9697 9696 9695 9795 9796 9896 9895 9894 9794 9793 9692 9592 9591 9691 9690 9689 9589 9590 9490 9390 9389 9489 9488 9388 9288 9289 9290 9291 9191 9192 9292 9392 9391 9491 9492 9493 9593 9693 9694 9594 9595 9596 9597 9598 9599 9499 9399 9398 9498 9497 9397 9396 9496 9494 9495 9395 9394 9393 9293 9193 9093 9092 9091 9090 9190 9189 9188 9187 9186 9185 9085 9086 9087 8987 8988 9088 9089 8989 8990 8991 8992 8993 8994 8995 9094 9194 9294 9295 9296 9297 9298 9299 9199 9099 8999 8899 8898 8798 8799 8699 8698 8697 8797 8897 8997 8998 9098 9198 9197 9097 9196 9195 9095 9096 8996 8896 8895 8894 8893 8892 8792 8791 8891 8890 8790 8789 8689 8688 8788 8889 8888 8887 8886 8986 8985 8885 8785 8786 8787 8687 8686 8685 8585 8586 8587 8588 8589 8590 8690 8691 8692 8693 8793 8794 8795 8796 8696 8695 8694 8594 8593 8595 8596 8496 8495 8494 8493 8492 8592 8591 8491 8490 8489 8488 8487 8387 8388 8288 8287 8286 8386 8486 8485 8385 8285 8185 8186 8187 8188 8088 8087 8086 8085 7985 7384 7383 7382 7381 7380 7379 6079 6080 6081 7885 7986 7987 7988 8189 8289 8389 8390 8290 8291 8391 8392 8292 8293 8393 8394 8294 8295 8395 8396 8296 8196 8195 8095 8096 7996 7896 7796 7795 7794 7894 7895 7995 7994 7993 7992 8092 8091 8093 8094 8194 8193 8192 8191 8190 8090 8089 7989 7990 7991 7891 7892 7893 7793 7792 7791 7790 7890 7889 7888 7887 7886 7786 7785 7685 7686 7687 7787 7789 7788 7688 7689 7690 7691 7692 7693 7694 7696 7695 7595 7596 7597 7598 7698 7697 7797 7798 7799 7899 7999 8099 8199 8299 8399 8499 8599 8598 8597 8497 8498 8398 8397 8297 8298 8198 8197 8097 8098 7998 7997 7897 7898 7699 7599 7499 7399 7398 7498 7497 7397 7396 7496 7495 7494 7594 7593 7493 7492 7592 7591 7590 7589 7588 7587 7586 7585 7485 7385 7285 7286 7386 7486 7487 7387 7287 7288 7388 7488 7489 7389 7289 7290 7390 7490 7491 7391 7291 7292 7392 7393 7394 7395 7294 7293 7193 7194 7195 7295 7296 7196 7197 7297 7298 7299 7199 7198 7098 7097 7096 7095 7094 7093 7092 7192 7191 7190 7090 7091 7089 7189 7188 7187 7186 7185 7085 6985 6885 6884 6984 7084 7184 7284 7283 7282 7281 7280 7279 7179 7079 6979 6879 6779 6279 6179 5283 5383 5482 6181 6180 6280 6579 6679 6780 6880 6980 6981 6983 7083 7183 7182 7181 7180 7080 7081 7082 6982 6883 6882 6881 6781 6782 6783 6784 6785 6786 6886 6986 7086 7087 7088 6989 6990 6988 6987 6887 6787 6687 6686 6685 6684 6683 6682 6681 6680 6580 6581 6481 6480 6479 6379 6380 6381 6281 6282 6182 6382 6383 6483 6482 6582 6583 6584 6484 6485 6585 6586 6587 6688 6788 6888 6889 6789 6689 6690 6790 6890 6891 6991 6992 6993 6994 6995 6996 6997 6998 7099 6999 6899 6898 6897 6896 6895 6894 6893 6892 6792 6793 6791 6691 6692 6591 6590 6589 6588 6488 6487 6486 6386 6286 6285 6385 6384 6284 6283 6183 6184 6084 6083 6082 5982 5882 5782 5682 5582 5483 5583 5683 5684 5584 5484 5384 5284 5285 5385 5485 5585 5685 5785 5784 5783 5883 5983 5984 5884 5885 5985 5986 5886 5987 5988 6088 6087 6086 6085 6185 6186 6187 6287 6387 6388 6288 6289 6389 6489 6490 6491 6492 6592 6593 6693 6794 6694 6594 6595 6695 6795 6796 6797 6799 6798 6696 6596 6496 6495 6395 6396 6394 6494 6493 6393 6392 6391 6390 6290 6291 6191 6190 6189 6188 6089 5989 5889 5888 5887 5787 5786 5686 5586 5486 5386 5286 5287 5288 5388 5387 5487 5587 5687 5688 5788 5789 5890 5990 6090 6091 6092 6192 6292 6293 6294 6194 6195 6295 6296 6196 6096 6095 6094 6193 6093 5993 5994 5995 5996 5896 5895 5894 5893 5892 5992 5991 5891 5791 5790 5689 5588 5488 5489 5589 5590 5690 5691 5692 5792 5793 5693 5593 5592 5591 5492 5392 5391 5491 5490 5390 5389 5289 5290 5291 5292 5293 5294 5394 5393 5493 5494 5594 5694 5794 5795 5796 5696 5695 5595 5596 5496 5495 5395 5295 5396 5296 5297 5397 5398 5298 5299 5399 5499 5498 5497 5597 5598 5599 5699 5698 5697 5797 5897 5997 6097 6197 6297 6398 6397 6497 6597 6697 6698 6699 6599 6598 6498 6499 6399 6299 6298 6198 6199 6099 5999 5899 5799 5798 5898 5998 6098
";
