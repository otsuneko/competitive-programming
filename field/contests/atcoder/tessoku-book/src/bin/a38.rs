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
        D:usize,
        N:usize,
        work:[(Usize1,Usize1,usize);N]
    }
    
    let mut max_t = vec![24;D];
    for &(L,R,H) in &work{
        for d in L..=R{
            max_t[d] = min(max_t[d],H);
        }
    }

    let ans = max_t.iter().sum::<usize>();
    println!("{}",ans);
}
