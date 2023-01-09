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
        N:usize,
        snow:[(Usize1,Usize1,Usize1,Usize1);N]
    }

    let mut imos = vec![vec![0;W+1];H+1];
    for t in 0..N{
        let (A,B,C,D) = snow[t];
        imos[A][B] += 1;
        imos[A][D+1] -= 1;
        imos[C+1][B] -= 1;
        imos[C+1][D+1] += 1;
    }

    let mut cumsum = vec![vec![0;W+1];H+1];

    for i in 0..H{
        for j in 0..W{
            cumsum[i+1][j+1] = imos[i][j];
        }
    }

    for i in 0..H{
        for j in 0..W{
            cumsum[i+1][j+1] += cumsum[i+1][j] + cumsum[i][j+1] - cumsum[i][j];
        }
    }

    for i in 1..=H{
        println!("{}",cumsum[i][1..].iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
    }

}
