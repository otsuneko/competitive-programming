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
    input! {N:usize}

    let mut s: Vec<String> = vec![String::from("");N+1];
    for i in 0..=N {
        let mut flg = true;
        for j in 1..=9 {
            if N%j == 0 && i % (N/j) == 0 {
                s[i] = j.to_string();
                flg = false;
                break
            }
        }
        if flg == true {
            s[i] = String::from("-");
        }
    }
    println!("{}",s.iter().join(""));
}
