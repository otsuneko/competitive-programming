#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;
use rustc_hash::FxHashMap;

const INF: usize = 1 << 60;
const MOD: usize = 1_000_000_007;

#[fastout]
fn main() {
    input! {
        S: Chars,
    }

    let mut dp = vec![0;8];
    let chokudai = "chokudai".chars().collect::<Vec<_>>();
    for c in S {
        if c == 'c' {
            dp[0] += 1;
            dp[0] %= MOD;
        }
        for i in 1..8 {
            if c == chokudai[i] {
                dp[i] += dp[i-1];
                dp[i] %= MOD;
            }
        }
    }

    println!("{}", dp[7]);
}
