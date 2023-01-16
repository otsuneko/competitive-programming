#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};
use::num_integer::Roots;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N:usize,
        M:usize
    }
    
    let mut reach_area:Vec<Vec<isize>> = vec![vec![-1;N];N];
    fn bfs(reach_area:&mut Vec<Vec<isize>>, n:usize, m:usize){
        let mut que = VecDeque::<(usize,usize)>::new();
        reach_area[0][0] = 0;
        que.push_back((0,0));
        while !que.is_empty(){
            let (y,x) = que.pop_front().unwrap();
            for ny in 0..n{
                if (ny as f64 - y as f64).abs().powf(2.0) > m as f64 * m as f64 {continue;}

                let dx = (m as f64 - (ny as f64 - y as f64).powf(2.0)).abs().sqrt();
                let nx = x as f64 + dx;
                if nx < n as f64 && (y as f64 - ny as f64).powf(2.0)+(x as f64 - nx as f64).powf(2.0) == m as f64{
                    let nx = nx as usize;
                    if reach_area[ny][nx] != -1{continue}
                    que.push_back((ny,nx));
                    reach_area[ny][nx] = reach_area[y][x] + 1
                }
                let nx = x as f64 - dx;
                if nx < n as f64 && (y as f64 - ny as f64).powf(2.0)+(x as f64 - nx as f64).powf(2.0) == m as f64{
                    let nx = nx as usize;
                    if reach_area[ny][nx] != -1{continue}
                    que.push_back((ny,nx));
                    reach_area[ny][nx] = reach_area[y][x] + 1
                }
            }
        }
    }
    
    bfs(&mut reach_area,N,M);

    for i in 0..N{
        println!("{}",reach_area[i].iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
    }


}
