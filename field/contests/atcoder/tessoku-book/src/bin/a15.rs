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
        mut A:[usize;N]
    }

    let mut cp = A.clone();
    cp.sort();
    cp.dedup();

    let mut A_compress = vec![];
    for a in A{
        A_compress.push(cp.binary_search(&a).unwrap()+1);
    }

    println!("{}",A_compress.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
}
