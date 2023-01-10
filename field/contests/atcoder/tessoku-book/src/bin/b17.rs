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
        H:[isize;N]
    }

    let mut dp:Vec<isize> = vec![INF as isize;N];
    dp[0] = 0;

    for i in 0..N{
        if i < N-1{
            dp[i+1] = min(dp[i+1],dp[i] + (H[i+1]-H[i]).abs());
        }
        if i < N-2{
            dp[i+2] = min(dp[i+2],dp[i] + (H[i+2]-H[i]).abs());
        }
    }

    let mut path:Vec<usize> = vec![];
    let mut idx = N-1;

    loop{
        path.push(idx+1);

        if idx == 0{break;}

        if dp[idx-1]+(H[idx]-H[idx-1]).abs() == dp[idx]{
            idx -= 1;
        }else{
            idx -= 2;
        }
    }

    path.reverse();

    println!("{}",path.len());
    println!("{}",path.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
}
