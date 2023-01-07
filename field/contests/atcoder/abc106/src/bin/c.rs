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
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        S:Chars,
        K:usize
    }

    for k in 0..K{
        if S[k] != '1'{
            println!("{}",S[k]);
            return
        }
    }
    println!("{}",S[K-1]);

    
}
