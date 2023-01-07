#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

#[fastout]
fn main() {
    input! {
        N:usize,
        M:usize,
        submit:[(usize,String);M]
    }

    let mut ac:HashSet<usize> = HashSet::default();
    let mut wa:HashMap<usize,usize> = HashMap::default();
    let mut wa_cnt = 0;

    for (a,s) in &submit{
        if s == "AC"{
            if !ac.contains(a){
                ac.insert(*a);
                wa_cnt += wa.get(a).unwrap_or(&0);
            }
        }else if s == "WA"{
            if !ac.contains(a){
                *wa.entry(*a).or_insert(0) = wa.get(a).unwrap_or(&0)+1;
            }
        }
    }

    println!("{} {}",ac.len(),wa_cnt);
}
