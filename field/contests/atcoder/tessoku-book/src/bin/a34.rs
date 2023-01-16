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
        X:usize,
        Y:usize,
        A:[usize;N]
    }

    let mut grundy = [0;100001];
    
    for i in 0..100001{
        let mut transit = [false;3];
        if i >= X{ transit[grundy[i-X]] = true; }
        if i >= Y{ transit[grundy[i-Y]] = true; }

        if transit[0] == false { grundy[i] = 0; }
        else if transit[1] == false{ grundy[i] = 1; }
        else{ grundy[i] = 2; }
    }

    let mut xor = 0;
    for i in 0..N{
        xor ^= grundy[A[i]];
    }

    if xor != 0 {
        println!("First");
    }else{
        println!("Second");
    }
}
