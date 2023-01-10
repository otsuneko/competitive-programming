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
        A:[usize;N-1],
        B:[usize;N-2]
    }

    let mut dp = vec![INF;N];
    dp[0] = 0;
    dp[1] = A[0];
    for i in 2..N{
        dp[i] = min(min(dp[i], dp[i-1]+A[i-1]),dp[i-2]+B[i-2]);
    }

    let mut path:Vec<usize> = vec![];
    let mut idx = N-1;
    loop{
        path.push(idx+1);
        
        if idx == 0{break;}

        if dp[idx-1] + A[idx-1] == dp[idx]{
            idx -= 1;
        }else{
            idx -= 2;
        }
    }

    path.reverse();

    println!("{}",path.len());
    println!("{}",path.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
    // println!("{:?}",dp);
}
