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

const MOVE: [(usize, usize); 4] = [(!0, 0), (0, 1), (1, 0), (0, !0)]; //縦横移動

#[fastout]
fn main() {
    input! {
        H: usize,
        W: usize,
        N: usize,
    }

    let mut grid = vec![vec!['.';W];H];
    let mut dir = 0;
    let (mut cy, mut cx) = (0,0);
    for _ in 0..N {
        if grid[cy][cx] == '.' {
            grid[cy][cx] = '#';
            dir = (dir + 1) % 4;
        } else {
            grid[cy][cx] = '.';
            dir = (dir + 3) % 4;
        }
        let (dy, dx) = MOVE[dir];
        cy = (cy + dy + H) % H;
        cx = (cx + dx + W) % W;
    }
    println!("{}",grid.iter().map(|x| x.iter().join("")).join("\n"));
}
