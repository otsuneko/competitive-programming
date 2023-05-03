#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
};

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N:usize,
        M:usize,
        A:[[usize;N];M]
    }

    let mut dp = vec![vec![INF;1<<N];M+1];
    dp[0][0] = 0;

    for i in 0..M{
        for j in 0..1<<N{
            let mut mask = j;

            for k in 0..N{
                if A[i][k] == 1{
                    mask |= 1<<k;
                }
            }

            dp[i+1][j] = min(dp[i+1][j], dp[i][j]);
            dp[i+1][mask] = min(dp[i+1][mask], dp[i][j] + 1);
        }
    }
    
    if dp[M][(1<<N)-1] == INF{
        println!("{}",-1);
    }else{
        println!("{}",dp[M][(1<<N)-1]);
    }

}

for bit in 0..(1<<N){

    let mut su = 0;

    for i in 0..N{
        if bit & (1<<i) == 1 {
            //ビットが立っているインデックスに対して何かする。
        }
    }
}