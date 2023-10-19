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
    input! {s: Bytes,}

    let n = s.len();
    let mut res = 0;
    for i in 0..n {
        for j in i+1..=n {
            let s = &s[i..j];
            let m = s.len();
            let mut f = true;
            for k in 0..m {
                f &= s[k] == s[m-k-1];
            }
            if f {
                res = res.max(m);
            }
        }
    }
    println!("{}",res);
}
