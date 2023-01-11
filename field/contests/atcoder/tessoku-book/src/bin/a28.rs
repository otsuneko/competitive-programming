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
        query:[(char,i64);N]
    }

    let mut ans:i64 = 0;
    let _mod = 10000;
    for &(op,a) in &query{
        match op {
            '+' => {ans = (ans+a)%_mod;}
            '-' => {ans = (ans-a+_mod)%_mod;}
            '*' => {ans = (ans*a)%_mod;}
            _ => {}
        }
        println!("{}",ans);
    }
}
