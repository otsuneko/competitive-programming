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
        A:[usize;N]
    }

    let mut dic:HashMap<usize, usize> = HashMap::new();
    for &a in &A{
        *dic.entry(a).or_insert(0) += 1;
    }

    let mut ans = 0;
    for (key,value) in &dic{
        ans += value*(value-1)/2;
    }
    println!("{}",ans);
}
