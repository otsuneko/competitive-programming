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
use rustc_hash::FxHashMap;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        S: Chars,
        T: Chars
    }

    let S = S.iter().map(|c| c.to_ascii_uppercase()).collect::<Vec<char>>();

    if T[T.len()-1] != 'X' {
        let mut i = 0;
        for t in &T {
            while i < S.len() && S[i] != *t {
                i += 1;
            }
            if i == S.len() {
                println!("No");
                return;
            }
            i += 1;
        }

    } else {
        let mut i = 0;
        for t in &T[..T.len()-1] {
            while i < S.len() && S[i] != *t {
                i += 1;
            }
            if i == S.len() {
                println!("No");
                return;
            }
            i += 1;
        }
    }

    println!("Yes");

}
