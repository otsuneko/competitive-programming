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

const INF: usize = 1 << 60;


pub struct UnionFind {
    parents: Vec<usize>,
    rank: Vec<usize> }

impl UnionFind {
    pub fn new(n: usize) -> UnionFind {
        UnionFind {
            parents: (0..n).collect::<Vec<usize>>(),
            rank: vec![1; n],
        }
    }

    pub fn find(&mut self, x: usize) -> usize {
        if self.parents[x] == x {
            return x;
        } else {
            let y = self.parents[x];
            let z = self.find(y);
            self.parents[x] = z;
            return z;
        }
    }

    pub fn union(&mut self, x: usize, y: usize) -> bool {
        let mut a = self.find(x);
        let mut b = self.find(y);
        if a == b { return false; }

        if self.rank[a] < self.rank[b] {
            std::mem::swap(&mut a, &mut b);
        }
        assert!(self.rank[a] >= self.rank[b]);

        self.rank[a] += self.rank[b];
        self.parents[b] = a;
        return true
    }

    pub fn size(&mut self, x: usize) -> usize {
        let y = self.find(x);
        self.rank[y]
    }

    pub fn same(&mut self, x: usize, y: usize) -> bool {
        self.find(x) == self.find(y)
    }

    pub fn members(&mut self, x: usize) -> Vec<usize> {
        let find = self.find(x);
        return (0..self.rank.len()).filter(|&i| self.find(i) == find).collect()
    }
}

#[fastout]
fn main() {
    input! {
        N:usize,
        K:usize,
        L:usize,
        road:[(Usize1,Usize1);K],
        rail:[(Usize1,Usize1);L],
    }

    let mut uf_road = UnionFind::new(N);
    let mut uf_rail = UnionFind::new(N);
    for (p,q) in road{
        uf_road.union(p,q);
    }
    for (r,s) in rail{
        uf_rail.union(r,s);
    }

    for i in 0..N{
        println!("{}",uf.size(i));
    }
}
