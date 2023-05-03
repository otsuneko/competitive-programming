#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::{Itertools, enumerate};
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
        A:[usize;N],
        D:usize,
        room:[(usize,usize);D]
    }

    let mut cummax = vec![0];
    for i in 0..N{
        cummax.push(max(cummax[i],A[i]));
    }

    let mut cummax_inv = vec![0];
    for i in (0..N).rev(){
        cummax_inv.push(max(cummax_inv[N-1-i],A[i]));
    }

    for (L,R) in room{
        let mut ans = 0;
        ans = max(ans, cummax[L-1]);
        ans = max(ans, cummax_inv[N-R]);

        println!("{}",ans);
    }



}
