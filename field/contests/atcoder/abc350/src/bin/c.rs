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
        N: usize,
        mut A: [usize;N],
    }

    let mut ans = vec![];
    loop {
        let mut cnt = 0;
        for i in 0..N {
            if A[i] != i+1 {
                let j = A[i]-1;
                A.swap(i, j);
                ans.push((min(i+1, j+1), max(i+1, j+1)));
                cnt += 1;
            }
        }
        if cnt == 0 {
            break;
        }
    }

    println!("{}", ans.len());
    for (a, b) in ans {
        println!("{} {}", a, b);
    }
}
