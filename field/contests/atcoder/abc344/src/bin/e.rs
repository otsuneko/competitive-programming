#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque, LinkedList},
    mem::swap,
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;
use rustc_hash::FxHashMap;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N: usize,
        mut A: [usize; N],
        Q: usize,
    }

    A.insert(0,0);
    A.push(INF);

    let mut front = FxHashMap::<usize,usize>::default();
    let mut back = FxHashMap::<usize,usize>::default();
    for val in A.windows(2) {
        front.insert(val[1], val[0]);
        back.insert(val[0], val[1]);
    }

    for _ in 0..Q {
        input!(q: usize);
        if q == 1 {
            input! {x:usize,y:usize}
            let b = back[&x];
            *back.get_mut(&x).unwrap() = y;
            *front.get_mut(&b).unwrap() = y;

            back.insert(y,b);
            front.insert(y,x);
        } else if q == 2 {
            input! {x:usize}
            let f = front[&x];
            let b = back[&x];
            *back.get_mut(&f).unwrap() = b;
            *front.get_mut(&b).unwrap() = f;
        }
    }

    let mut ans = vec![];
    let mut cur = 0;
    while back[&cur] != INF {
        cur = back[&cur];
        ans.push(cur);
    }

    println!("{}",ans.iter().join(" "));
}
