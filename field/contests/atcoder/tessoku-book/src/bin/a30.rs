#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: usize = 1 << 60;

const MOD: usize = 1_000_000_007;
fn modpow(n:usize, m:usize, _mod:usize) -> usize {
    if m == 0 { return 1 }
    let mut res = modpow(n*n%_mod, m/2, _mod);
    if m%2 == 1{
        res = &res*n%_mod;
    }
    return res
}

fn nCr(n:usize, r:usize) -> usize{
    let mut numera = 1; // 分子
    let mut denomi = 1; // 分母

    for i in 0..r{
        numera = (numera*(n-i))%MOD;
        denomi = (denomi*(i+1))%MOD;
    }
    return numera * modpow(denomi, MOD-2, MOD) % MOD;
}

#[fastout]
fn main() {
    input! {
        n:usize,
        r:usize
    }
    println!("{}",nCr(n,r));
}
