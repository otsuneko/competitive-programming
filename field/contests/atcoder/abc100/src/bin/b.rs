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
        D:usize,
        N:usize
    }

    let mut cnt = 0;
    for i in 1..10i32.pow(7){
        if D == 0{
            if i%100 != 0{
                cnt += 1
            }
        }else if D == 1{
            if i%100 == 0 && i%10000 != 0{
                cnt += 1
            }
        }else{
            if i%10000 == 0 && i%1000000 != 0{
                cnt += 1
            }
        }
        if cnt == N{
            println!("{}",i);
            return
    }

    }

}
