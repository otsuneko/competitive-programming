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
        T: Usize1,
        edges: [(Usize1, Usize1); N-1]
    }
    
    let mut graph = vec![vec![];N];
    for &(A,B) in &edges{
        graph[A].push(B);
        graph[B].push(A);
    }
    
    let mut dp = vec![0;N];
    fn dfs(s:usize, pre:usize, graph:&Vec<Vec<usize>>, dp:&mut Vec<usize>) {
        for &to in &graph[s] {
            if to != pre {
                dfs(to,s, graph, dp);
                dp[s] = max(dp[s], dp[to]+1);
            }
        }
    }
    
    dfs(T,INF, &graph, &mut dp);

    println!("{}",dp.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
}
