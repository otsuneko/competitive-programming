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
        A:[[usize;N];2],
    }

    let mut dp = vec![vec![0;N];2];
    dp[0][0] = A[0][0];
    dp[1][0] = dp[0][0] + A[1][0];

    for i in 0..2{
        for j in 0..N-1{
            if i == 0{
                dp[i+1][j] = max(dp[i+1][j],dp[i][j] + A[i+1][j]);
            }
            dp[i][j+1] = max(dp[i][j+1], dp[i][j] + A[i][j+1]);
        }
    }

    println!("{}",dp[1][N-1]);

}
