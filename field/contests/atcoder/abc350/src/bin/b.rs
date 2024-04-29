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

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N: usize,
        Q: usize,
        T: [usize;Q],
    }

    let mut teeth = vec![true;N];
    for t in T {
        teeth[t-1] = !teeth[t-1];
    }

    // trueの数をカウント
    let ans = teeth.iter().filter(|&&t| t).count();
    println!("{}", ans);

}
