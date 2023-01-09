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
        N:f64
    }

    fn is_ok(mid: f64, N: f64) -> bool {
        // 問題ごとに引数・条件を定義する。
        if mid.powf(3.0) + mid > N{
            return true;
        }else{
            return false;
        } 
    }

    // 初期値のng,okを受け取り,is_okを満たす最小(最大)のokを返す。
    // まずis_okを定義すべし。
    // ng ok は  とり得る最小の値-1 とり得る最大の値+1。
    // 最大最小が逆の場合はよしなにひっくり返す。
    let mut ok:f64 = 100_000.0;
    let mut ng:f64 = 0.0;
    while (ok-ng).abs() > 0.001{
        let mid:f64 = (ok + ng)/2.0;
        if is_ok(mid,N){
            ok = mid;
        }else{
            ng = mid;
        }
    }

    println!("{}",ok);

}
