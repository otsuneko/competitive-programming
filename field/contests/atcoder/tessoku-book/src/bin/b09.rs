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
        paper:[(usize,usize,usize,usize);N]
    };

    let (mut H,mut W) = (0,0);
    for (A,B,C,D) in &paper{
        H = max(H,*C+2);
        W = max(W,*D+2);
    }

    let mut imos = vec![vec![0;W];H];
    for (A,B,C,D) in &paper{
        imos[*A][*B] += 1;
        imos[*A][*D] -= 1;
        imos[*C][*B] -= 1;
        imos[*C][*D] += 1;
    }

    let mut cumsum = vec![vec![0;W+1];H+1];

    for i in 0..H{
        for j in 0..W{
            cumsum[i+1][j+1] = imos[i][j];
        }
    }

    for i in 0..H{
        for j in 0..W{
            cumsum[i+1][j+1] += cumsum[i+1][j] + cumsum[i][j+1] - cumsum[i][j];
        }
    }

    let mut ans = 0;
    for i in 0..H+1{
        for j in 0..W+1{
            if cumsum[i][j] > 0{
                ans += 1;
            }
        }
    }
    // println!("{}",cumsum.iter().map(|x| x.iter().join(" ")).join("\n"));
    println!("{}",ans);

}
