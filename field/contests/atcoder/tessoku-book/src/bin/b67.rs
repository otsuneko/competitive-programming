#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use petgraph::unionfind::UnionFind;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N: usize,
        M: usize,
        mut edges: [(Usize1, Usize1, usize); M]
    }
    
    // クラスカル法
    // edges: 辺集合[始点, 終点, 重み]
    edges.sort_by_key(|&x| Reverse(x.2));
    let mut weight = 0;
    let mut nodes = BTreeSet::<usize>::new();
    let mut uf = UnionFind::<usize>::new(N);
    for &(s,t,w) in &edges{
        if !uf.equiv(s,t){
            uf.union(s,t);
            weight += w;
            nodes.insert(s);
            nodes.insert(t);
        }
    }
    
    println!("{}",weight);
    // println!("{}",nodes.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
    
}
