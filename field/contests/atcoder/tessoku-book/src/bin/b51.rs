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
        S:Chars
    }

    let mut stack = vec![];

    for i in 0..S.len(){
        if S[i] == '('{
            stack.push((i+1,'('));
        }else{
            let (n,bracket) = stack.pop().unwrap();
            println!("{} {}",n,i+1);
        }
    }

}
