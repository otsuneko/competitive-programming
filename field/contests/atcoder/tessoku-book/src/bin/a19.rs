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
        W:usize,
        goods:[(usize,usize);N]
    }

    let mut dp = vec![vec![0;W+1];N+1];

    for i in 0..N{
        for j in 0..W+1{
            if j + goods[i].0 <= W{
                dp[i+1][j+goods[i].0] = max(dp[i+1][j+goods[i].0], dp[i][j] + goods[i].1);
            }
            dp[i+1][j] = max(dp[i+1][j], dp[i][j]);
        }
    }

    let mut ans = 0;
    for w in 0..W+1{
        ans = max(ans, dp[N][w]);
    }
    println!("{}",ans);
}
