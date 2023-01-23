#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N:usize,
        X:Usize1,
        Y:Usize1
    }

    let mut ans = vec![0;N-1];

    let mut graph = vec![vec![];N];
    for i in 0..N-1{
        graph[i].push((i+1,1));
        graph[i+1].push((i,1)); // 有向グラフの場合はコメントアウトする。
    }
    graph[X].push((Y,1));
    graph[Y].push((X,1));

    for i in 0..N{
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

        dijkstra(N, &graph, i, &mut dist, &mut prev);

        for j in i+1..N{
            ans[dist[j]-1] += 1;
        }

    }

    for &a in &ans{
        println!("{}",a);
    }

}
