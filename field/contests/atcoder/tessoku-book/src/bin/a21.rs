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
        block:[(Usize1,usize);N]
    }

    let mut dp = vec![vec![0;N];N];
    for LEN in (0..N).rev() {
        for l in 0..N-LEN {
            let r = l + LEN;
            if l > 0{
                let score1 = if l <= block[l-1].0 && block[l-1].0 <= r {block[l-1].1} else {0};
                dp[l][r] = max(dp[l][r], dp[l-1][r] + score1);    
            }
            if r < N-1{
                let score2 = if l <= block[r+1].0 && block[r+1].0 <= r {block[r+1].1} else {0};
                dp[l][r] = max(dp[l][r], dp[l][r+1] + score2);    
            }
        }
    }

    let mut ans = 0;
    for i in 0..N{
        ans = max(ans, dp[i][i]);
    }
    println!("{}",ans);

}
