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
        S: Chars
    }

    let mut flg = true;
    if S[0] != '<' || S[S.len()-1] != '>' {
        flg = false;
    }

    if !&S[1..S.len()-1].iter().all(|&c| c == '=') {
        flg = false;
    }

    if flg {
        println!("Yes");
    }else{
        println!("No");
    }
}
