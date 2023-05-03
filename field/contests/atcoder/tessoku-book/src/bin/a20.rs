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
    let mut dp = vec![vec![0;LT+1];LS+1];

    // LCS(最長共通部分列)をDPで求める
    for i in 0..LS{
        for j in 0..LT{
            if S[i] == T[j]{
                dp[i+1][j+1] = max(max(dp[i][j+1], dp[i+1][j]), dp[i][j]+1);
            }else{
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j]);
            }
        }
    }

    // 復元処理
    let mut res:Vec<char> = vec![];
    let (mut i, mut j) = (LS,LT);
    while i > 0 && j > 0{
        if S[i-1] == T[j-1]{
            res.push(S[i-1]);
            i -= 1;
            j -= 1;
        }else if dp[i][j] == dp[i-1][j]{
            i -= 1;
        }else if dp[i][j] == dp[i][j-1]{
            j -= 1;
        }
    }
    res.reverse();
    let res = res.iter().join("");

    println!("{}",dp[LS][LT]);

}
