#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use memoise::memoise_map;
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

// メモ化再帰
#[memoise_map(n)]
fn dfs(n:u64,A:u64,X:f64,Y:f64) -> f64{
    if n == 0 {
        return 0.0;
    }
    let res1 = dfs(n/A,A,X,Y) + X;
    let res2 = (2..=6).map(|i| dfs(n/i,A,X,Y)).sum::<f64>()/5.0 + Y*6.0/5.0;
    let res = res1.min(res2);
    return res;
}

#[fastout]
fn main() {
    input! {
        N: u64,
        A: u64,
        X: f64,
        Y: f64,
    }

    let ans = dfs(N,A,X,Y);

    println!("{}", ans);

}
