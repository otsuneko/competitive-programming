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
use rustc_hash::FxHashMap;

const INF: usize = 1 << 60;
const MOVE: [(usize, usize); 4] = [(!0, 0), (1, 0), (0, !0), (0, 1)]; //縦横移動
// const MOVE: [(usize, usize); 8] = [(!0, !0), (!0, 0), (!0, 1), (0, !0), (0, 1), (1, !0), (1, 0), (1, 1)]; // 縦横斜め移動

fn bfs(R:usize, C:usize, sy:usize, sx:usize, gy:usize, gx:usize, maze:&Vec<Vec<char>>, dist:&mut Vec<Vec<isize>>) -> isize{
    let mut que = VecDeque::<(usize,usize)>::new();
    que.push_back((sy,sx));
    dist[sy][sx] = 0;
    while !que.is_empty(){
        let (y,x) = que.pop_front().unwrap();
        if (y,x) == (gy,gx){
            return dist[gy][gx];
        }
        for (dy,dx) in MOVE {
            let (ny,nx) = (y+dy, x+dx);
            if ny < R && nx < C && maze[ny][nx] != '#' && dist[ny][nx] == -1{
                dist[ny][nx] = dist[y][x] + 1;
                que.push_back((ny,nx));
            }
        }
    }

    return -1;
}

#[fastout]
fn main() {
    input! {
        (R,C):(usize,usize),
        (sy,sx,gy,gx):(Usize1,Usize1,Usize1,Usize1),
        maze:[Chars;R]
    }

    let mut dist:Vec<Vec<isize>> = vec![vec![-1; C]; R];
    let ans = bfs(R,C,sy,sx,gy,gx,&maze, &mut dist);
    println!("{}",ans);
}
