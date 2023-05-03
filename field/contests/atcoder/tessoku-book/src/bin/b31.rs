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
        N:usize
    }

    let div3 = N/3;
    let div5 = N/5;
    let div7 = N/7;
    let div15 = N/15;
    let div21 = N/21;
    let div35 = N/35;
    let div105 = N/105;
    println!("{}",div3+div5+div7-div15-div21-div35+div105);
}
