#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: usize = 1 << 60;

// 拝借元　https://github.com/kenkoooo/competitive-programming-rs/blob/master/src/graph/maximum_flow.rs
pub mod dinitz {
    const INF: i64 = 1 << 60;
    pub struct Edge {
        pub to: usize,
        pub rev: usize,
        pub is_reversed: bool,
        pub cap: i64,
    }

    pub struct Dinitz {
        pub g: Vec<Vec<Edge>>,
    }

    impl Dinitz {
        pub fn new(v: usize) -> Dinitz {
            let mut g: Vec<Vec<Edge>> = Vec::new();
            for _ in 0..v {
                g.push(Vec::new());
            }
            Dinitz { g }
        }

        pub fn add_edge(&mut self, from: usize, to: usize, cap: i64) {
            let to_len = self.g[to].len();
            let from_len = self.g[from].len();
            self.g[from].push(Edge {
                to,
                rev: to_len,
                is_reversed: false,
                cap,
            });
            self.g[to].push(Edge {
                to: from,
                rev: from_len,
                is_reversed: true,
                cap: 0,
            });
        }

        fn dfs(
            &mut self,
            v: usize,
            sink: usize,
            flow: i64,
            level: &[i32],
            iter: &mut [usize],
        ) -> i64 {
            if v == sink {
                return flow;
            }
            while iter[v] < self.g[v].len() {
                let flow = std::cmp::min(flow, self.g[v][iter[v]].cap);
                let to = self.g[v][iter[v]].to;
                if flow > 0 && level[v] < level[to] {
                    let flowed = self.dfs(to, sink, flow, level, iter);
                    if flowed > 0 {
                        let rev = self.g[v][iter[v]].rev;
                        self.g[v][iter[v]].cap -= flowed;
                        self.g[to][rev].cap += flowed;
                        return flowed;
                    }
                }
                iter[v] += 1;
            }
            0
        }

        fn bfs(&self, s: usize) -> Vec<i32> {
            let v = self.g.len();
            let mut level = vec![-1; v];
            level[s] = 0;
            let mut deque = std::collections::VecDeque::new();
            deque.push_back(s);
            while let Some(v) = deque.pop_front() {
                for e in self.g[v].iter() {
                    if e.cap > 0 && level[e.to] < 0 {
                        level[e.to] = level[v] + 1;
                        deque.push_back(e.to);
                    }
                }
            }
            level
        }

        pub fn max_flow(&mut self, s: usize, t: usize) -> i64 {
            let v = self.g.len();
            let mut flow: i64 = 0;
            loop {
                let level = self.bfs(s);
                if level[t] < 0 {
                    return flow;
                }
                let mut iter = vec![0; v];
                loop {
                    let f = self.dfs(s, t, INF, &level, &mut iter);
                    if f == 0 {
                        break;
                    }
                    flow += f;
                }
            }
        }
    }
}

#[fastout]
fn main() {
    input! {
        N:usize,
        C:[Chars;N]
    }

    let s = 2*N;
    let t = s+1;
    let mut flow = dinitz::Dinitz::new(2*N+2);
    for i in 0..N{
        flow.add_edge(s, i, 1);
        flow.add_edge(N+i, t, 1);
        for j in 0..N{
            if C[i][j] == '#'{
                flow.add_edge(i, N+j, 1);
            }
        }
    }

    println!("{}",flow.max_flow(s,t));
}
