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

    let mut seen = vec![false;N];
    fn dfs(s:usize, graph:&Vec<Vec<usize>>, seen:&mut Vec<bool>){
        seen[s] = true;
        for &to in &graph[s]{
            if seen[to] == false{
                dfs(to, graph, seen);
            }
        }
    }

    dfs(0,&graph,&mut seen);
    
    if seen.iter().any(|x| *x == false) {
        println!("The graph is not connected.");
    }else{
        println!("The graph is connected.");
    }
}
