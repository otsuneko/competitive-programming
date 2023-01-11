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
        X:Usize1,
        mut A:Chars
    }

    let mut deq = VecDeque::new();
    deq.push_back(X);
    A[X] = '@';

    while !deq.is_empty(){
        let pos = deq.pop_front().unwrap();
        if pos > 0 && A[pos-1] == '.'{
            A[pos-1] = '@';
            deq.push_back(pos-1);
        }
        if pos < N-1 && A[pos+1] == '.'{
            A[pos+1] = '@';
            deq.push_back(pos+1);
        }
    }
    println!("{}",A.iter().join(""));

}
