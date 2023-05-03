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
        Q:usize,
        A:[usize;N],
        query:[(usize,usize);Q]
    }

    let mut cumsum = vec![0];
    for i in 0..N{
        cumsum.push(cumsum[i] + A[i])
    }

    for (L,R) in query{
        println!("{}",cumsum[R]-cumsum[L-1]);
    }


}
