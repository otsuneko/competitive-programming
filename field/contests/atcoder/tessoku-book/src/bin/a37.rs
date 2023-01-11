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
        M:usize,
        B:usize,
        A:[usize;N],
        C:[usize;M]
    }

    let ans = N*M*B + M*A.iter().sum::<usize>() + N*C.iter().sum::<usize>();
    println!("{}",ans);
}
