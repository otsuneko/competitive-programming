#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit, vec,
};

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N:usize,
        W:usize,
        goods:[(usize,usize);N]
    }

    let mut dp = vec![vec![INF;N*1000+1];N+1];
    dp[0][0] = 0;

    for i in 0..N{
        for j in 0..(N*1000+1){
            dp[i+1][j] = min(dp[i+1][j], dp[i][j]);
            if j+goods[i].1 <= N*1000{
                dp[i+1][j+goods[i].1] = min(dp[i+1][j+goods[i].1], dp[i][j] + goods[i].0);
            }
        }
    }

    // println!("{}",dp.iter().map(|x| x.iter().join(" ")).join("\n"));

    let mut ans = 0;
    for v in 0..N*1000+1{
        if dp[N][v] <= W{
            ans = v;
        }
    }    

    println!("{}",ans);
}
