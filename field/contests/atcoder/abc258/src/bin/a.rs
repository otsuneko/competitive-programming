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

const INF: usize = 1 << 60;

#[fastout]
#[allow(non_snake_case, non_upper_case_globals, path_statements)]
fn main() {
    input! {
        K:usize
    }

    if K >= 60{
        print!("22:");
        println!("{:0>2}",(K-60));
    }else{
        print!("21:");
        println!("{:0>2}",K);
    };
}
