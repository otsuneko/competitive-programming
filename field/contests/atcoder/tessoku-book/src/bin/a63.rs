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

let mut dist:Vec<isize> = vec![-1;N];
fn bfs(s:usize, graph:&Vec<Vec<usize>>, dist:&mut Vec<isize>){
    let mut que = VecDeque::<usize>::new();
    que.push_back(s);
    dist[s] = 0;
    while !que.is_empty(){
        let s = que.pop_front().unwrap();
        for &to in &graph[s]{
            if dist[to] != -1 {continue}
            dist[to] = dist[s] + 1;
            que.push_back(to);
        }
    }
}

bfs(0,&graph, &mut dist);

    for &d in &dist{
        println!("{}",d);
    }

    
}
