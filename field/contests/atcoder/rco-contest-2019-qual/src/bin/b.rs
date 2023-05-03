#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input, marker::{Chars, Bytes, Isize1, Usize1},source::line::LineSource};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit,
    io::{prelude::*, BufReader}, vec
};
use itertools::Itertools;
use superslice::Ext;
use lazy_static::lazy_static;

// 定数
const INF: usize = 1 << 60;
const MOVE:[[isize;2];4] = [[1, 0], [-1, 0], [0, 1], [0, -1]];

macro_rules! input(($($tt:tt)*) => (
    let stdin = std::io::stdin();  // Rust1.60までは分けて記述必要
    let mut stdin = proconio::source::line::LineSource::new(stdin.lock());
    proconio::input!(from &mut stdin, $($tt)*);
));

lazy_static! {
    static ref _INPUT: (usize, usize) = {
        input! { n:usize, m:usize, } (n, m)
    };
    static ref N: usize = _INPUT.0;
    static ref M: usize = _INPUT.1;
}

fn search_connectable_area(sy:usize, sx:usize, quality_grid:&mut Vec<Vec<usize>>, score_grid:&mut Vec<Vec<usize>>, heap:&mut BinaryHeap<(usize,usize,usize)>) {
    let base_quality = quality_grid[sy][sx];
    let mut que = VecDeque::<(usize,usize,usize)>::new();
    que.push_back((sy,sx,quality_grid[sy][sx]));
    let (mut max_score, mut max_y, mut max_x) = (base_quality,sy,sx);
    while !que.is_empty(){
        let (y,x,quality) = que.pop_front().unwrap();
        for &[dy,dx] in &MOVE{
            let (ny,nx) = (y as isize + dy, x as isize + dx);
            if 0 <= ny && ny < *N as isize && 0 <= nx && nx < *N as isize && quality_grid[ny as usize][nx as usize] == base_quality && score_grid[ny as usize][nx as usize] == 0 {
                let new_score = quality+quality_grid[ny as usize][nx as usize];
                que.push_back((ny as usize, nx as usize, new_score));
                score_grid[ny as usize][nx as usize] = new_score;
                if new_score > max_score {
                    (max_score, max_y, max_x) = (new_score, ny as usize, nx as usize);
                }
            }
        }
    }
    // 最高スコアの情報(score,y,x)をheapに入れる
    heap.push((max_score, max_y, max_x));
}

#[fastout]
fn main() {
    lazy_static::initialize(&_INPUT);
    let mut quality_grid:Vec<Vec<usize>> = {
        input! { mut _quality_grid:[[usize;*N];*N]} _quality_grid
    };

    // 手入れ
    let mut ans = vec![];
    'out:for y in 0..*N{
        for x in 0..*N{
            let diff;
            if 2 <= quality_grid[y][x] && quality_grid[y][x] <= 3 {
                diff = 3 - quality_grid[y][x];
            } else if 4 <= quality_grid[y][x] && quality_grid[y][x] <= 6 {
                diff = 6 - quality_grid[y][x];
            } else if 6 <= quality_grid[y][x] && quality_grid[y][x] <= 9 {
                diff = 9 - quality_grid[y][x];
            } else {
                diff = 0;
            }
            for i in 0..diff{
                ans.push(vec![1,y,x]);
                if ans.len() == 2500{
                    break 'out;
                }    
            }
            quality_grid[y][x] += diff;
        }
    }
    
    // 収穫の順序決め準備
    let mut heap = BinaryHeap::<(usize,usize,usize)>::new();
    let mut score_grid = vec![vec![0;*N];*N];
    for y in 0..*N{
        for x in 0..*N{
            if score_grid[y][x] > 0 { continue }
            search_connectable_area(y, x, &mut quality_grid, &mut score_grid, &mut heap);
        }
    }

    // 収穫
    while ans.len() < 2500 {
        let (total_quality,y,x) = heap.pop().unwrap();
        ans.push(vec![2,y,x]);
    }

    for a in ans{
        println!("{}",a.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
    }

    // debug
    // for y in 0..*N{
    //     println!("{}",quality_grid[y].iter().map(|x| x.to_string()).collect::<Vec<_>>().join(","));
    // }

    // for y in 0..*N{
    //     println!("{}",score_grid[y].iter().map(|x| x.to_string()).collect::<Vec<_>>().join(","));
    // }
}
