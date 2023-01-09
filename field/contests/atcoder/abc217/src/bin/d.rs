#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        L:usize,
        Q:usize,
        query:[(usize,usize);Q]
    }

    let mut bts:BTreeSet<usize> = BTreeSet::new();
    bts.insert(0);
    bts.insert(L);

    for (c,x) in query{
        if c == 1{
            bts.insert(x);
        }else if c == 2{
            let left = bts.range(..x).next_back().unwrap();
            let right = bts.range(x..).next().unwrap();
            println!("{}",right-left);
        }
    }
}
