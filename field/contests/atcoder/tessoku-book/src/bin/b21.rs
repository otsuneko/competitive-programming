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
        S:Chars
    }

    let mut dp = vec![vec![0;N];N];
    for i in 0..N{dp[i][i] = 1;}
    for i in 0..N-1{
        dp[i][i+1] = if S[i]==S[i+1] {2} else {1};
    }

    for LEN in 2..N{
        for l in 0..N-LEN{
            let r = l+LEN;
            dp[l][r] = max(dp[l][r-1], dp[l+1][r]);
            if S[l] == S[r]{
                dp[l][r] = max(dp[l][r], dp[l+1][r-1] + 2);
            }
        }
    }

    println!("{}",dp[0][N-1]);

}
