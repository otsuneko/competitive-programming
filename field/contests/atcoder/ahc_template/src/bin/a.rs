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
use rand::Rng;

const INF: usize = 1 << 60;
const TIME_LIMIT: f64 = 3.0;

pub struct Solver {
    // 問題固有のパラメータ
}

impl Solver {
    pub fn new() -> Self {
        Self {
            // 問題固有のパラメータ
        }
    }

    pub fn solve(&self) {

        // 時間計測
        get_time();

        // 乱数生成器
        let mut rng = rand_pcg::Pcg64Mcg::seed_from_u64(890482);

    }
}

#[fastout]
fn main() {
    input! {}

    let solver = Solver::new();
    solver.solve();
}

////////////////////////////////////////
// ここから下はテンプレート
////////////////////////////////////////
pub fn get_time() -> f64 {
	static mut STIME: f64 = -1.0;
	let t = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap();
	let ms = t.as_secs() as f64 + t.subsec_nanos() as f64 * 1e-9;
	unsafe {
		if STIME < 0.0 {
			STIME = ms;
		}
		ms - STIME
	}
}
