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
        A:[Usize1;N-1],
        B:[Usize1;N-1]
    }

    let mut dp = vec![-1;N];
    dp[0] = 0;

    for i in 0..N-1{
        if dp[i] > -1{
            dp[A[i]] = max(dp[A[i]], dp[i]+100);
            dp[B[i]] = max(dp[B[i]], dp[i]+150);    
        }
    }

    println!("{}",dp[N-1]);
}
