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
        K:usize,
        N:usize,
        A:[usize;N]
    }
    let mut ma = 0;
    for i in 0..N{
        if i == N-1{
            ma = max(ma, K-A[N-1] + A[0])
        }else{
            ma = max(ma, A[i+1]-A[i])
        }
    }
    println!("{}",K-ma);
}
