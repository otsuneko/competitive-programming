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
        N:usize,
        K:usize,
        A:[usize;N]
    }

    fn is_ok(mid: isize,K:usize, A:&Vec<usize>) -> bool {
        // 問題ごとに引数・条件を定義する。
        let mut paper = 0;
        for a in A{
            paper += mid/(*a) as isize;
        }
        if paper >= K as isize{
            return true;
        }else{
            return false;
        } 
    }

    // 初期値のng,okを受け取り,is_okを満たす最小(最大)のokを返す。
    // まずis_okを定義すべし。
    // ng ok は  とり得る最小の値-1 とり得る最大の値+1。
    // 最大最小が逆の場合はよしなにひっくり返す。
    let mut ok:isize = 10_000_000_000 as isize;
    let mut ng:isize = -1;
    while (ok-ng).abs() > 1{
        let mid:isize = (ok + ng)/2;
        if is_ok(mid,K,&A){
            ok = mid;
        }else{
            ng = mid;
        }
    }

    println!("{}",ok);
}
