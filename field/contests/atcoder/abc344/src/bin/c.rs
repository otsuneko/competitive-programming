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
    input! {
        N: usize,
        A: [usize;N],
        M: usize,
        B: [usize;M],
        L: usize,
        C: [usize;L],
        Q: usize,
        X: [usize;Q]
    }

    let mut s = HashSet::new();
    for a in A.iter() {
        for b in B.iter() {
            for c in C.iter() {
                s.insert(a+b+c);
            }
        }
    }

    for x in X.iter() {
        if s.contains(x){
            println!("Yes");
        } else {
            println!("No");
        }
    }
}
