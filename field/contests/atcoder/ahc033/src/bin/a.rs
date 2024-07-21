#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit,
    time::Instant
};
use itertools::Itertools;
use superslice::Ext;
use rustc_hash::FxHashMap;

const TIME_LIMIT: f64 = 3.0;
const INF: usize = usize::MAX;

// #[derive(Clone,Debug)]
// struct State {
//     container_pos: Vec<(usize,usize)>,
//     crane_pos: Vec<(usize,usize)>,
// }

#[derive(Clone,Debug)]
struct Solver {
    n: usize,
    a: Vec<Vec<i64>>,
    start_time: Instant,
    current_time: Instant,
    best_score: i64,
    ans: Vec<Vec<char>>,
}

impl Solver {
    fn new(n: usize, a: Vec<Vec<i64>>) -> Self {
        Solver {
            n,
            a,
            start_time: Instant::now(),
            current_time: Instant::now(),
            best_score: 0,
            ans: vec![vec![];n],
        }
    }

    fn solve(&mut self) {

        self.greedy_choice();

        // ansの各要素をStringに変換して出力
        self.ans.iter().for_each(|s| {
            println!("{}", s.iter().collect::<String>());
        });
    }

    fn greedy_choice(&mut self) {
        // 1. 20個のコンテナを5x4のマスに配置する
        for i in 0..self.n {
            self.ans[i].extend(vec!['P','R','R','R','Q','L','L','L','P','R','R','Q','L','L','P','R','Q']);
        }

        // 2. クレーン1～4を爆破する
        self.ans[0].extend(vec!['.']);
        for i in 1..self.n {
            self.ans[i].extend(vec!['B']);
        }

        // 3. クレーン0だけで、コンテナをなるべく順番どおりに移動する
        let mut crane_pos = vec![0,1];
        let mut container_pos = vec![vec![0,0];25];
        for i in 0..5 {
            for j in 0..5 {
                container_pos[i*5+j] = vec![i,j];
            }
        }

        let mut next_container = vec![0,5,10,15,20];
        let mut finished_num = 0;
        while finished_num < 25 {
            // 一番近くにある次に搬出すべきコンテナを探す
            let mut min_dist = 100;
            let mut min_idx = 0;
            for i in 0..5 {
                let dist = next_container[i] - i;
                if dist < min_dist {
                    min_dist = dist;
                    min_idx = i;
                }
            }
        }

    }

    fn calc_score(&self, a: &[Vec<i64>]) -> i64 {
        let score = 0;
        score
    }
}

fn main() {
    input! {
        n: usize,
        a: [[i64; n]; n],
    }

    let mut solver = Solver::new(n, a);
    solver.solve();
}
