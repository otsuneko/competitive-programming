#![allow(dead_code)]
#[allow(unused_imports)]
use itertools::Itertools;
#[allow(unused_imports)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
#[allow(unused_imports)]
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals, path_statements)]
fn main() {
    input! {
        N:usize,
        A:[usize;N]
    }

    let mut ans = 0;
    for a in &A{
        ans += a.trailing_zeros();
    }
    println!("{}",ans);

}
