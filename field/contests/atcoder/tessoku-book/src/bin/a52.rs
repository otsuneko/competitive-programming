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
        Q:usize,
    }

    let mut deque = VecDeque::new();

    for _ in 0..Q{
        input!{
            n:usize
        }
        if n == 1{
            input!{x:String}
            deque.push_back(x);
        }else if n == 2{
            println!("{}",deque[0]);
        }else{
            deque.pop_front();
        }
    }
}
