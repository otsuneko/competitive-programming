#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: isize = 100000;

#[fastout]
fn main() {
    input! {
        N:usize,
        A:[usize;N]
    }

    let mut dp = vec![vec![0;N+1];N+1];

    for i in 0..N{
        dp[N][i] = A[i];
    }

    for i in (0..N).rev(){
        for j in 0..=i{
            if i%2==1{
                dp[i][j] = max(dp[i+1][j], dp[i+1][j+1]);
            }else{
                dp[i][j] = min(dp[i+1][j], dp[i+1][j+1]);
            }
        }
    }

    println!("{}",dp[1][0]);

}
