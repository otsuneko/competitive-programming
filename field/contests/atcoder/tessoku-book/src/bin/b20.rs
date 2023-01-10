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
        S:Chars,
        T:Chars
    }

    let (LS,LT) = (S.len(),T.len());
    let mut dp = vec![vec![INF;LT+1];LS+1];
    for i in 0..=LS{ dp[i][0] = i}
    for j in 0..=LT{ dp[0][j] = j}

    // 編集距離(レーベンシュタイン距離)をDPで求める
    for i in 0..LS{
        for j in 0..LT{
            dp[i+1][j+1] = min(min(dp[i][j+1]+1, dp[i+1][j]+1), dp[i][j] + if S[i] == T[j] {0} else {1});
        }
    }

    println!("{}",dp[LS][LT]);

}
