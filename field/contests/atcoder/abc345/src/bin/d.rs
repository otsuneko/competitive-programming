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
use once_cell::sync::Lazy;

const INF: usize = 10;

fn dfs(grid: &mut Vec<Vec<usize>>, idx: usize) {

    // 最後のタイルまで確認終えたら条件を満たしているかチェック
    if idx == *N {
        let mut flg = true;
        'outer: for y in 0..*H {
            for x in 0..*W {
                if grid[y][x] == INF {
                    flg = false;
                    break 'outer;
                }
            }
        }
        if flg == true {
            println!("Yes");
            exit(0);
        }
        return;
    }

    // println!("{}",grid.iter().map(|x| x.iter().join(" ")).join("\n"));

    for y in 0..*H {
        for x in 0..*W {
            // 既にタイルが置かれていたらスキップ
            if grid[y][x] != INF {
                continue;
            }

            // idx番目のタイルがそのままの向きで置けるかどうか判定
            if y+tiles[idx][0] <= *H && x+tiles[idx][1] <= *W {
                let mut flg = true;
                'outer: for dy in 0..tiles[idx][0] {
                    for dx in 0..tiles[idx][1] {
                        if grid[y+dy][x+dx] != INF {
                            flg = false;
                            break 'outer;
                        }
                    }
                }
                // そのままの向きで置く
                if flg == true {
                    for dy in 0..tiles[idx][0] {
                        for dx in 0..tiles[idx][1] {
                            grid[y+dy][x+dx] = idx;
                        }
                    }
                    dfs(grid, idx+1);
                    // 後処理
                    for dy in 0..tiles[idx][0] {
                        for dx in 0..tiles[idx][1] {
                            grid[y+dy][x+dx] = INF;
                        }
                    }
                }
            }

            // idx番目のタイルの縦横の長さが異なりかつ逆向きで置けるかどうか判定
            if tiles[idx][0] != tiles[idx][1] && y+tiles[idx][1] <= *H && x+tiles[idx][0] <= *W {
                let mut flg = true;
                'outer: for dy in 0..tiles[idx][1] {
                    for dx in 0..tiles[idx][0] {
                        if grid[y+dy][x+dx] != INF {
                            flg = false;
                            break 'outer;
                        }
                    }
                }
                // 逆向きで置く
                if flg == true {
                    for dy in 0..tiles[idx][1] {
                        for dx in 0..tiles[idx][0] {
                            grid[y+dy][x+dx] = idx;
                        }
                    }
                    dfs(grid, idx+1);
                    // 後処理
                    for dy in 0..tiles[idx][1] {
                        for dx in 0..tiles[idx][0] {
                            grid[y+dy][x+dx] = INF;
                        }
                    }
                }
            }

            // 何も置かずに次へ
            dfs(grid, idx+1);

        }
    }

}

static N: Lazy<usize> = Lazy::new(|| {
    input! {
        n: usize,
    }
    n
});

static H: Lazy<usize> = Lazy::new(|| {
    input! {
        h: usize,
    }
    h
});

static W: Lazy<usize> = Lazy::new(|| {
    input! {
        w: usize,
    }
    w
});

static tiles: Lazy<Vec<Vec<usize>>> = Lazy::new(|| {
    let n = *N;
    input! {
        t: [[usize;2];n],
    }
    t
});

#[fastout]
fn main() {
    // 初期化順序を指定
    let _n = *N;
    let _h = *H;
    let _w = *W;
    let _tiles = &tiles;

    let mut grid = vec![vec![INF;*W];*H];

    dfs(&mut grid, 0);
    println!("No");

}
