#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit, vec,
};

const INF: usize = 1 << 60;

fn sieve(n:usize) -> Vec<usize>{
    let mut is_prime = vec![true;n+1];
    is_prime[0] = false;
    is_prime[1] = false;

    let mut table = vec![];
    for i in 2..=n{
        if !is_prime[i] { continue }
        table.push(i);
        for j in (i*2..=n).step_by(i){
            is_prime[j] = false;
        }
    }
    return table
}

fn divisor(n:usize) -> Vec<usize>{
    let mut res = vec![];
    for i in (1..).take_while(|x| x*x <= n){
        if n%i == 0{
            res.push(i);
            if i*i != n{
                res.push(n/i);
            }
        }
    }
    res.sort();
    return res;
}

#[fastout]
fn main() {
    input! {
        N:usize
    }

    // println!("{}",sieve(N).iter().join("\n"));
    println!("{:?}",divisor(N));

}
