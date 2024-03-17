#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        T:String,
        N:usize,
    }

    let mut A = vec![];
    for _ in 0..N {
        input!{
            a:usize,
            S:[String;a]
        }
        A.push(S);
    }

    dbg!(&N);

    let mut dic = HashMap::<String,usize>::new();
    dic.insert(String::from(""), 0);
    for i in 0..N {
        for (s,n) in dic.clone().into_iter() {
            for add_s in A[i].iter() {
                let ns = s.clone() + add_s;
                // println!("{} {}",ns,n);
                if T.starts_with(&ns) {
                    let min_val = min(*dic.get(&ns).unwrap_or(&usize::MAX), n + 1);
                    dic.insert(ns, min_val);
                }
            }
        }
    }

    let mut ans = INF;
    for item in dic.iter() {
        let (s,n) = item;
        if *s == T{
            ans = min(ans,*n);
        }
    }

    if ans == INF {
        println!("-1");
    }else {
        println!("{}",ans);
    }
}
