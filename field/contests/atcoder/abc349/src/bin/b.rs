#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit, vec,
};
use itertools::Itertools;
use superslice::Ext;
use rustc_hash::FxHashMap;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        S: Chars,
    }

    let mut count = HashMap::new();
    for c in &S {
        *count.entry(c).or_insert(0) += 1;
    }

    let mut pattern = vec![0; S.len()+1];
    for c in count.values() {
        pattern[*c] += 1;
    }

    for i in 0..=S.len() {
        if !(pattern[i] == 0 || pattern[i] == 2) {
            println!("No");
            return;
        }
    }
    println!("{}", "Yes");
}
