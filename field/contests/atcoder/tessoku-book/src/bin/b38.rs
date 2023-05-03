#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: usize = 1 << 60;

#[fastout]
fn main() {
    input! {
        N:usize,
        S:Chars
    }

    let mut H = vec![0;N];
    for i in 0..N-1{
        if S[i] == 'A'{
            H[i+1] = H[i] + 1;
        }else{
            H[i+1] = H[i] - 1;
        }
    }

    // println!("{:?}",H);

    let mi = H.iter().min().unwrap();
    let mut H2:Vec<i32> = H.iter().map(|x| x+(1-mi)).collect();

    let sub = H2[0]-1;
    for i in 0..N-1{
        if S[i] == 'A'{
            H2[i] -= sub;
        }else{
            break
        }
    }

    let sub = H2[N-1]-1;
    for i in (0..N-1).rev(){
        if S[i] == 'B'{
            H2[i] -= sub;
        }else{
            break
        }
    }

    // println!("{:?}",H2);

    let ans = H2.iter().sum::<i32>();
    println!("{}",ans);
}
