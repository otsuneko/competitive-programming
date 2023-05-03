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
        T:usize,
        N:usize,
        p:[(usize,usize);N]
    }

    let mut imos = vec![0;T+1];
    for (L,R) in p{
        imos[L] += 1;
        imos[R] -= 1;
    }

    let mut cumsum = vec![0];
    for i in 0..T{
        cumsum.push(cumsum[i] + imos[i]);
        println!("{}",cumsum[i+1]);
    }

}
