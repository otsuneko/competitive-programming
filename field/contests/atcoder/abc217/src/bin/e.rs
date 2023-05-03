#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        Q:usize
    }

    let mut deque = VecDeque::new();
    let mut heap = BinaryHeap::new();

    for _ in 0..Q{
        input! {n:usize};
        if n == 1{
            input! {x:usize}
            deque.push_back(x);
        }else if n == 2{
            if let Some(Reverse(top)) = heap.pop() {
                println!("{}",top);
            }else{
                let top = deque.pop_front().unwrap();
                println!("{}",top);
            }
        }else{
            while let Some(x) = deque.pop_front(){
                heap.push(Reverse(x));
            }
        }
    }

}
