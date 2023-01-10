#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
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
        A:[usize;N-1],
        B:[usize;N-2]
    }

    let mut dp = vec![INF;N];
    dp[0] = 0;

    for i in 0..N{
        if i >= 1{
            dp[i] = min(dp[i], dp[i-1]+A[i-1]);
        }
        if i >= 2{
            dp[i] = min(dp[i], dp[i-2]+B[i-2]);
        }
    }

    println!("{}",dp[N-1]);
}
