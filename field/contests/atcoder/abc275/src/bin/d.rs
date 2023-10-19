#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

// use recur_fn::{recur_fn, RecurFn};
use memoise::memoise;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {N: i64}

    #[memoise(n <= 100000000000)]
    fn rec(n: i64) -> i64 {
        if n == 0 {
            return 1
        } else {
            return rec(n/2) + rec(n/3)
        }
    }

    println!("{}", rec(N));
    
}
