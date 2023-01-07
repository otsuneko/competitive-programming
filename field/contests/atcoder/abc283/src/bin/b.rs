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
        N:usize,
        mut A:[usize;N],
        Q:usize,
    }

    let mut query = vec![];
    for _ in 0..Q {
        input! {
            t: usize,
        }
        if t == 1 {
            input! {
                k: Usize1, x: usize,
            }
            query.push((t, Some(k), Some(x)));
        } else if t == 2 {
            input! {
                k: Usize1,
            }
            query.push((t, Some(k), None));
        }
    }

    for (t,k,x) in query{
        if t == 1{
            A[k.unwrap()] = x.unwrap();
        } else if t == 2{
            println!("{}",A[k.unwrap()]);
        }

    }

}
