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

    let mut count = HashMap::new();
    for c in &S {
        *count.entry(c).or_insert(0) += 1;
    }

    let mut seen = HashSet::new();

    let mut ans:usize = if count.len() == S.len() { 0 } else { 1 };

    for (c1,n1) in &count {
        for (c2,n2) in &count {
            if !seen.contains(&(c1,c2)) && c1 != c2 {
                ans += n1 * n2;
            }
            seen.insert((c1,c2));
            seen.insert((c2,c1));
        }
    }

    println!("{}",ans);

}
