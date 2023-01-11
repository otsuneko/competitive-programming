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
        (R,C):(isize,isize),
        (sy,sx,gy,gx):(Isize1,Isize1,Isize1,Isize1),
        maze:[Chars;R]
    }
    
    let mut dist:Vec<Vec<isize>> = vec![vec![-1;C as usize];R as usize];
    fn bfs(R:isize, C:isize, sy:isize, sx:isize, gy:isize, gx:isize, maze:&Vec<Vec<char>>, dist:&mut Vec<Vec<isize>>){
        let MOVE = [[1, 0], [-1, 0], [0, 1], [0, -1]];
        // let MOVE = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]; // 縦横斜め移動
        let mut que = VecDeque::<(isize,isize)>::new();
        que.push_back((sy,sx));
        dist[sy as usize][sx as usize] = 0;
        while !que.is_empty(){
            let (y,x) = que.pop_front().unwrap();
            if (y,x) == (gy,gx){
                println!("{}",dist[gy as usize][gx as usize]);
                exit;
            }
            for &[dy,dx] in &MOVE{
                let (ny,nx) = (y+dy,x+dx);
                if 0 <= ny && ny < R && 0 <= nx && nx < C && maze[ny as usize][nx as usize] != '#' && dist[ny as usize][nx as usize] == -1{
                    dist[ny as usize][nx as usize] = dist[y as usize][x as usize] + 1;
                    que.push_back((ny,nx));
                }
            }
        }
    }
    
    bfs(R,C,sy,sx,gy,gx,&maze, &mut dist);

}
