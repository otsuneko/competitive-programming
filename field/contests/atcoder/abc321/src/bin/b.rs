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

#[fastout]
fn main() {
    input! {
        N:usize,
        X:usize,
        A:[usize;N-1]
    }

    let ans = (0..=100)
        .find(|&x| {
            let mut A = A.iter().copied().chain(std::iter::once(x)).collect_vec();
            A.sort();
            X <= A[1..N-1].iter().sum()
        })
        .map_or_else(|| -1, |x| x as i64);
    println!("{}",ans);
}
