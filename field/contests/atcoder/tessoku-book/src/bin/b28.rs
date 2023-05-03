#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit, vec,
};

const INF: usize = 1 << 60;
const MOD: usize = 1_000_000_007;

fn fib(n:usize) -> usize{
    let mut ans = vec![0;n];
    ans[0] = 1;
    ans[1] = 1;
    for i in 2..n{
        ans[i] = (ans[i-1] + ans[i-2])%MOD;
    }

    ans[n-1]
}

#[fastout]
fn main() {
    input! {
        N:usize
    }

    println!("{}",fib(N));


}
