#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use petgraph::algo::dijkstra;
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
            edges: [(Usize1, Usize1, usize); M]
        }
        
        let mut graph = vec![vec![];N];
        for &(A,B,C) in &edges{
            graph[A].push((B,C));
            graph[B].push((A,C));
        }
    
        // ダイクストラ法での最短経路算出(計算量はO((E+V)logV))
        let mut dist = vec![INF;N];
        let mut prev = vec![INF;N];
        fn dijkstra(n:usize, graph:&Vec<Vec<(usize,usize)>>, s:usize, dist:&mut Vec<usize>, prev:&mut Vec<usize>) {
            let mut heap = BinaryHeap::new();
            heap.push((Reverse(0),s));
            dist[s] = 0;
            while !heap.is_empty() {
                let (Reverse(cost),v) = heap.pop().unwrap();
                if dist[v] < cost{ continue }
                for &(to, cost) in &graph[v] {
                    if dist[v] + cost < dist[to] {
                        dist[to] = dist[v] + cost;
                        heap.push((Reverse(dist[to]), to));
                        prev[to] = v;
                    }
                }
            }
        }
    
        // 最短経路復元
        fn get_path(mut t: usize, dist:&Vec<usize>, prev:&Vec<usize>) -> Vec<usize> {
            let mut path = vec![];
            if dist[t] == INF { return path }
            while t != INF {
                path.push(t+1);
                t = prev[t];
            }
            path.reverse();
            return path
        }
    
        dijkstra(N, &graph, 0, &mut dist, &mut prev);

        let path = get_path(N-1, &dist, &prev);
        println!("{}",path.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
}
