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
        K:usize
    }

    let mut A = vec![0;N+1];
    for i in 1..=N {
        A[i] = i - i
            .to_string()
            .chars()
            .into_iter()
            .map(|c| c.to_digit(10).unwrap() as usize)
            .sum::<usize>()
    }

    let lv = 1<<5;
    let mut dp = vec![vec![0;N+1];lv+1]; //10^9 < 2^32
    for i in 1..=N { dp[0][i] = A[i]; }
    for d in 0..lv {
        for i in 1..=N {
            dp[d+1][i] = dp[d][dp[d][i]];
        }
    }
    
    for i in 1..=N {
        let mut cur = i;
        for d in (0..lv).rev() {
            if (K / (1<<d)) % 2 == 1 {
                cur = dp[d][cur];
            }
        }
        println!("{}",cur);
    }
}
