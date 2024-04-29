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
        N: usize,
        votes: [[usize;3]; N]
    }

    let su = votes.iter().map(|v| v[2]).sum::<usize>();
    let mut dp = vec![vec![INF; su+1]; N];

    if votes[0][0] > votes[0][1] {
        dp[0][votes[0][2]] = 0;
    } else {
        dp[0][votes[0][2]] = (votes[0][1] - votes[0][0] + 1) / 2;
        dp[0][0] = 0;
    }

    for i in 1..N {
        for j in 0..=su {
            if dp[i-1][j] == INF {
                continue;
            }

            if votes[i][0] > votes[i][1] {
                dp[i][j+votes[i][2]] = dp[i-1][j];
            } else {
                dp[i][j] = min(dp[i][j],dp[i-1][j]);
                dp[i][j+votes[i][2]] = dp[i-1][j] + (votes[i][1] - votes[i][0] + 1) / 2;
            }
        }
    }

    let mut ans = INF;
    for i in su/2+1..=su {
        ans = min(ans, dp[N-1][i]);
    }

    println!("{}", ans);


}
