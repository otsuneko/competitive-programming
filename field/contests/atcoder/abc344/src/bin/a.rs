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
        S: String
    }

    let mut ans = String::new();
    let mut flg = false;
    for c in S.chars() {
        if flg == false && c == '|' {
            flg = true;
            continue
        }
        if flg == true && c == '|' {
            flg = false;
            continue
        }
        if flg == true {
            continue
        }
        ans.push(c);
    }

    println!("{}", ans);
}
