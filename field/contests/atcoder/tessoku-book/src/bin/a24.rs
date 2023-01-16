#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use superslice::Ext;
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

    let mut L = vec![]; // L[x]:長さx+1の部分列の最後の要素として考えられる最小値
    let mut ans = 0;
    for i in 0..N{
        let pos = L.lower_bound(&(A[i]));
        // let pos = L.upper_bound(&(A[i])); // 広義単調増加

        if pos == ans{
            L.push(A[i]);
            ans += 1;
        }else{
            L[pos] = A[i];
        }
    }

    println!("{}",ans);
    
}
