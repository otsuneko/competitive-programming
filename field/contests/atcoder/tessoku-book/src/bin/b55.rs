#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: isize = 1 << 60;
const NINF: isize = -1 << 60;

#[fastout]
fn main() {
    input! {
        Q:usize,
    }

    let mut set = BTreeSet::new();
    for _ in 0..Q{
        input! {
            n:isize
        }
        if n == 1{
            input! {
                x:isize
            }
            set.insert(x);
        }else{
            input! {
                x:isize
            }
            let upper = set.range(x..).next().unwrap_or(&INF);
            let lower = set.range(..=x).next_back().unwrap_or(&NINF);
            if (upper,lower) == (&INF,&NINF){
                println!("{}",-1);
            }else{
                println!("{}",min(upper-x,x-lower));
            }
        }
    }
}
