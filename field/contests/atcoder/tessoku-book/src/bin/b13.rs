#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit, vec,
};

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N:usize,
        K:usize,
        A:[usize;N]
    }

    let mut q:VecDeque<usize> = VecDeque::new();
    let mut su = 0;
    let mut ans = 0;
    for &c in &A{
        q.push_back(c); //dequeの右端に要素を一つ追加する。
        //(追加した要素に応じて何らかの処理を行う)
        su += c;

        while !(su <= K){
            let rm = q.pop_front().unwrap(); //条件を満たさないのでdequeの左端から要素を取り除く
            //(取り除いた要素に応じて何らかの処理を行う)
            su -= rm;
        }
        //(何らかの処理を行う。whileがbreakしたので、dequeに入っている連続部分列は条件を満たしている。特に右端の要素から左に延ばせる最大の長さになっている。)
        ans += q.len()
    }

    println!("{}",ans);
}
