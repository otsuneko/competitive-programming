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
        H:usize,
        W:usize,
        X:[[i64;W];H],
        Q:usize,
        query:[(usize,usize,usize,usize);Q]
    }

    let mut cumsum = vec![vec![0;W+1];H+1];

    for i in 0..H{
        for j in 0..W{
            cumsum[i+1][j+1] = X[i][j];
        }
    }

    for i in 0..H{
        for j in 0..W{
            cumsum[i+1][j+1] += cumsum[i+1][j] + cumsum[i][j+1] - cumsum[i][j];
        }
    }

    for (L1,R1,L2,R2) in query{
        println!("{}",cumsum[L2][R2] - cumsum[L1-1][R2] - cumsum[L2][R1-1] + cumsum[L1-1][R1-1]);
    }

}
