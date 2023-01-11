#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: usize = 1 << 60;

fn is_prime(n: usize) -> bool {
    n != 1 && (2..).take_while(|i| i*i <= n).all(|i| n%i != 0)
}

#[fastout]
fn main() {
    input! {
        Q:usize,
        X:[usize;Q]
    }

    for &x in &X{
        if is_prime(x) {
            println!("Yes");
        }else{
            println!("No");
        }
    }
}
