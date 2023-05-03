#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
    io::{stdin, stdout, Write, BufWriter},
};

const INF: usize = 1 << 60;
#[fastout]
fn main() {
    input! {
        H:usize,
        W:usize,
        C:[Chars;H]
    }

    let mut dp:[[usize;31];31] = [[0;31];31];
    dp[0][0] = 1;

    for i in 0..H{
        for j in 0..W{
            if C[i][j] == '#'{ continue }
            if i > 0{
                dp[i][j] += dp[i-1][j];
            }
            if j > 0{
                dp[i][j] += dp[i][j-1];
            }
        }
    }

    // println!("{}",dp.iter().map(|x| x.iter().join(" ")).join("\n"));
    println!("{}",dp[H-1][W-1]);

}
