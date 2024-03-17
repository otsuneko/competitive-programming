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

const INF: usize = 1 << 60;

#[fastout]
fn main() {

    let mut A = Vec::<usize>::new();

    loop {
        input! {
            n: usize
        }
        A.push(n);
        if n == 0 {
            break
        }
    }

    for i in 0..A.len() {
        println!("{}",A[A.len()-1-i]);
    }
}
