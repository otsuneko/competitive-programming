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

#[fastout]
fn main() {
    input! {
        h: usize, w: usize,
        s: [Chars; h],}

    let moves = [(1, 0), (-1, 0), (0, 1), (0, -1)];

    let mut bfs = |sy: usize, sx: usize| -> i64 {
        let mut queue = VecDeque::new();
        queue.push_back((sy, sx));
        let mut visited = vec![vec![false; w]; h];
        let mut visited2 = vec![vec![false; w]; h];
        let mut visited_dir = vec![vec![HashSet::new(); w]; h];
        visited[sy][sx] = true;
        visited2[sy][sx] = true;
        for &(dy, dx) in &moves {
            visited_dir[sy][sx].insert((dy, dx));
        }
        let mut res = 1;
        while let Some((y, x)) = queue.pop_front() {
            // 周囲に磁石がないことの判定
            let mut has_magnet = false;
            for &(dy, dx) in &moves {
                let ny = (y as i64 + dy) as usize;
                let nx = (x as i64 + dx) as usize;
                if ny < h && nx < w && s[ny][nx] == '#' {
                    has_magnet = true;
                    break;
                }
            }
            if !has_magnet {
                for &(dy, dx) in &moves {
                    let ny = (y as i64 + dy) as usize;
                    let nx = (x as i64 + dx) as usize;
                    if ny < h && nx < w && s[ny][nx] == '.' {
                        if !visited[ny][nx] {
                            visited[ny][nx] = true;
                            visited2[ny][nx] = true;
                            visited_dir[ny][nx].insert((dy, dx));
                            queue.push_back((ny, nx));
                            res += 1;
                        } else if !visited2[ny][nx] && !visited_dir[ny][nx].contains(&(dy, dx)) {
                            visited2[ny][nx] = true;
                            visited_dir[ny][nx].insert((dy, dx));
                            res += 1;
                        }
                    }
                }
            }
        }
        res
    };

    let mut ans = 1;
    let mut visited = vec![vec![false; w]; h];
    let mut visited_dir = vec![vec![HashSet::<(usize,usize)>::new(); w]; h];
    for y in 0..h {
        for x in 0..w {
            if s[y][x] != '.' || visited[y][x] {
                continue;
            }
            // 周囲に磁石がある場合は移動できない
            let mut has_magnet = false;
            for &(dy, dx) in &moves {
                let ny = (y as i64 + dy) as usize;
                let nx = (x as i64 + dx) as usize;
                if ny < h && nx < w && s[ny][nx] == '#' {
                    has_magnet = true;
                    break;
                }
            }
            if !has_magnet {
                ans = ans.max(bfs(y, x));
            }
        }
    }
    println!("{}", ans);
}
