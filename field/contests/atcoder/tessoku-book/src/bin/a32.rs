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
        A:usize,
        B:usize
    }

    let mut dp = vec![false;N+1];
    for i in 0..=N{
        if dp[i] { continue }
        if i+A <= N { dp[i+A] = true; }
        if i+B <= N {dp[i+B] = true; }
    }

    if dp[N] == true {
        println!("First");
    }else{
        println!("Second");
    }
    
}
