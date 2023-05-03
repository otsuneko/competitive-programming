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
        N: usize,
        M: usize,
        edges: [(Usize1, Usize1); M]
    }
    
    let mut graph = vec![vec![];N];
    for &(A,B) in &edges{
        graph[A].push(B);
        graph[B].push(A);
    }
    
    for i in 0..N{
        print!("{}: {{",i+1);
        print!("{}",graph[i].iter().map(|x| (x+1).to_string()).collect::<Vec<_>>().join(", "));
        println!("}}");
    }
}
