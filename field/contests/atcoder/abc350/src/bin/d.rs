#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use petgraph::graph;
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

fn bfs(s:usize, graph:&Vec<Vec<usize>>, dist:&mut Vec<isize>) -> (usize, usize){
    let mut que = VecDeque::<usize>::new();
    que.push_back(s);
    dist[s] = 0;
    let mut vert = 1;
    let mut edge = 0;
    while !que.is_empty(){
        let s = que.pop_front().unwrap();
        for &to in &graph[s]{
            edge += 1;
            if dist[to] != -1 {continue}
            dist[to] = dist[s] + 1;
            que.push_back(to);
            vert += 1;
        }
    }

    return (vert, edge);
}

#[fastout]
fn main() {
    input! {
        N: usize,
        M: usize,
        friends: [(Usize1, Usize1);M],
    }

    let mut graph = vec![vec![];N];
    for (a, b) in friends {
        graph[a].push(b);
        graph[b].push(a);
    }

    let mut ans = 0;
    let mut dist:Vec<isize> = vec![-1;N];
    for i in 0..N{
        if dist[i] != -1 {continue}
        let (vert, edge) = bfs(i,&graph, &mut dist);
        ans += vert*(vert-1)/2 - edge/2;
    }

    println!("{}",ans);

}
