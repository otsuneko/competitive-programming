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

fn gcd(a: usize, b: usize) -> usize {
    if b == 0 {
        a
    } else {
        gcd(b, a % b)
    }
}

fn gcd_list(list: &[usize]) -> usize {
    list.iter().fold(list[0], |a, b| gcd(a, *b))
}

fn lcm(a: usize, b: usize) -> usize {
    a / gcd(a, b) * b
}

fn lcm_list(list: &[usize]) -> usize {
    list.iter().fold(list[0], |a, b| lcm(a, *b))
}

#[fastout]
#[allow(non_snake_case, non_upper_case_globals, dead_code)]
fn main() {
    input! {
        N:usize,
        A:[usize;N]
    }

    let mut ans = 0;

    for a in A{
        ans += a-1;
    }

    println!("{}",ans);
}
