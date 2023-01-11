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
        L:usize,
        R:usize,
        X:[usize;N]
    }

    let mut set: BTreeSet<usize> = BTreeSet::new();
    for &x in &X{
        set.insert(x);
    }

    let mut dic = HashMap::new();
    for (i,x) in X.iter().enumerate(){
        dic.insert(x, i);
    }

    let mut dp = vec![-1;N+1];
    dp[0] = 0;

    for i in 0..N {
        if dp[i] >= 0{
            let cur = if i > 0 {X[i-1]} else {0};
            let next:Vec<&usize> = set.range(cur+L..=(cur+R)).collect();
            for &x in &next{
                let idx = dic.get(x).unwrap();
                dp[idx+1] = dp[i] + 1;
            }
        }
    }

    println!("{}",dp[N]);

}
