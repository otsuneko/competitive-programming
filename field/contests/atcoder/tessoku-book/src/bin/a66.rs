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
        N:usize,
        Q:usize,
    }

    let mut uf = UnionFind::<usize>::new(N);

    for _ in 0..Q{
        input! {
            t:usize,
            u:Usize1,
            v:Usize1
        }
        if t == 1{
            uf.union(u, v);
        }else{
            if uf.equiv(u, v) {
                println!("Yes");
            }else{
                println!("No");
            }
        }
    }
}
