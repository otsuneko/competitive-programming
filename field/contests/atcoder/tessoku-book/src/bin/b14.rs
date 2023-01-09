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
        K:usize,
        A:[usize;N]
    }

    let B = &A[..N/2];
    let C = &A[N/2..];

    let mut set1 = HashSet::<usize>::new();
    let mut set2 = HashSet::<usize>::new();

    for bit in 0..(1<<B.len()){
        let su:usize = (0..B.len())
            .filter(|x| (bit & (1<<x)) != 0)
            .map(|x| B[x])
            .sum();
        set1.insert(su);
    }

    for bit in 0..(1<<C.len()){
        let su:usize = (0..C.len())
            .filter(|x| (bit & (1<<x)) != 0)
            .map(|x| C[x])
            .sum();
        set2.insert(su);
    }

    for n in set1{
        if set2.contains(&(K-n)){
            println!("{}","Yes");
            return
        }
    }

    println!("{}","No");
}
