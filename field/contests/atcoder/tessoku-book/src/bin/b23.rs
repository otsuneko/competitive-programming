#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use num_integer::Roots;
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
        city:[(isize,isize);N]
    }

    fn dist(pos1:(isize,isize),pos2:(isize,isize)) -> f64{
        (((pos2.0-pos1.0)*(pos2.0-pos1.0) + (pos2.1-pos1.1)*(pos2.1-pos1.1)) as f64).sqrt()
    }

    let mut dp = vec![vec![INF as f64;N];1<<N];
    dp[0][0] = 0.0;

    for bit in 0..1<<N{
        for s in 0..N{
            for t in 0..N{
                if bit != 0 && bit & (1<<s) == 0 {continue}
                if bit & (1<<t) == 0 && s != t{
                    dp[bit | 1<<t][t] = dp[bit | 1<<t][t].min(dp[bit][s] + dist(city[s],city[t]));
                }
            }
        }
    }

    println!("{}",dp[(1<<N)-1][0]);

}
