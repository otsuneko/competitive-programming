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
    }

    let mut graph = vec![HashSet::<usize>::new();N];
    for _ in 0..M{
        input! {k:usize}
        input! {tmp:[usize;k]}
        for i in 0..k{
            for j in i+1..k{
                graph[tmp[i]-1].insert(tmp[j]-1);
                graph[tmp[j]-1].insert(tmp[i]-1);
            }
        }
    }

    for g in graph{
        if g.len() != N-1{
            println!("{}","No");
            return
        }
    }
    println!("{}","Yes");

}
