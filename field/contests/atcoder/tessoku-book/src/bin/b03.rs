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
        A:[usize;N]
    }

    for i in 0..N{
        for j in i+1..N{
            for k in j+1..N{
                if A[i]+A[j]+A[k] == 1000{
                    println!("{}","Yes");
                    return
                }
            }
        }
    }
    println!("{}","No");
}
