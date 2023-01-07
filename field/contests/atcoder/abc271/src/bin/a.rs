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

// "def base10int(value, base):",
// "    if value >= base:",
// "        return base10int(value//base, base) + str(value % base)",
// "    return str(value % base)",

fn base10int(value:usize,base:usize) -> String{
    let quotient = value/base;
    let remainder = value%base;
    if value >= base{
        return base10int(quotient, base) + &std::char::from_digit(remainder as u32, base as u32).unwrap().to_string().to_uppercase()
    }
    return std::char::from_digit(remainder as u32, base as u32).unwrap().to_string().to_uppercase();
}

#[fastout]
#[allow(non_snake_case, non_upper_case_globals, path_statements)]
fn main() {
    input! {N:usize}

    println!("{:0>2}",base10int(N, 16));
}
