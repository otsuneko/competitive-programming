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
        A:[usize;N],
        B:[usize;N],
        C:[usize;N],
        D:[usize;N]
    }

    let mut E = HashSet::<usize>::new();
    let mut F = HashSet::<usize>::new();

    for &a in &A{
        for &b in &B{
            E.insert(a+b);
        }
    }

    for &c in &C{
        for &d in &D{
            F.insert(c+d);
        }
    }

    for &e in &E{
        if F.contains(&(K-e)) {
                println!("{}","Yes");
                return
        }
    }
    println!("{}","No");
}
