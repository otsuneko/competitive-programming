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

// #[fastout]
#[allow(non_snake_case, non_upper_case_globals, path_statements)]
fn main() {
    input! {
        S:String
    }

    match S.as_str(){
        "Monday" => println!("{}",5),
        "Tuesday" => println!("{}",4),
        "Wednesday" => println!("{}",3),
        "Thursday" => println!("{}",2),
        "Friday" => println!("{}",1),
        _ => println!("{}",0)
    }
}
