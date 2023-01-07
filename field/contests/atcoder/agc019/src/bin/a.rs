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
        Q:usize,
        H:usize,
        S:usize,
        D:usize,
        N:usize
    }

    if N == 1{
        println!("{}",min(min(Q*4,H*2),S));
    }else{
        // Dが一番安くてNが奇数の場合
        if D*N/2 <= Q*4*N && D*N/2 <= H*2*N && D*N/2 <= S*N && N%2 == 1{
            println!("{}",D*(N-1)/2 + min(min(Q*4,H*2),S));
        }else{
            println!("{}",min(min(min(Q*4*N,H*2*N),S*N),D*N/2));
        }
    }
}
