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
        S:usize,
        A:[usize;N]
    }

    let mut dp = vec![vec![false;S+1];N+1];
    dp[0][0] = true;

    for i in 0..N{
        for j in 0..S+1{
            if dp[i][j] == true && j + A[i] <= S{
                dp[i+1][j+A[i]] = true;
            }
            dp[i+1][j] |= dp[i][j];
        }
    }

    if dp[N][S] {
        println!("Yes");
    }else{
        println!("No");
    }
}
