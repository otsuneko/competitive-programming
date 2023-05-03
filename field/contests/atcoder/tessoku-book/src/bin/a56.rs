#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: usize = 1 << 60;

use rand::Rng;
// 拝借元：https://github.com/kenkoooo/competitive-programming-rs/blob/master/src/string/rolling_hash.rs
pub mod rolling_hash {
    const MASK_30: u64 = (1 << 30) - 1;
    const MASK_31: u64 = (1 << 31) - 1;
    const MOD: u64 = (1 << 61) - 1;

    pub struct RollingHash {
        hash: Vec<u64>,
        pow: Vec<u64>,
    }

    impl RollingHash {
        pub fn new(s: &[u8], base: u64) -> RollingHash {
            let n = s.len();
            let mut hash: Vec<u64> = vec![0; n + 1];
            let mut pow: Vec<u64> = vec![0; n + 1];
            pow[0] = 1;
            for i in 0..n {
                pow[i + 1] = modulo(mod_mul(pow[i], base));
                hash[i + 1] = modulo(mod_mul(hash[i], base) + s[i] as u64);
            }
            RollingHash { hash, pow }
        }

        /// Get hash of [l, r)
        pub fn get_hash(&self, l: usize, r: usize) -> u64 {
            modulo(self.hash[r] + MOD - mod_mul(self.hash[l], self.pow[r - l]))
        }
    }

    fn mod_mul(a: u64, b: u64) -> u64 {
        let (a_prefix, a_suffix) = (a >> 31, a & MASK_31);
        let (b_prefix, b_suffix) = (b >> 31, b & MASK_31);
        let m = a_suffix * b_prefix + a_prefix * b_suffix;
        modulo(a_prefix * b_prefix * 2 + (m >> 30) + ((m & MASK_30) << 31) + a_suffix * b_suffix)
    }

    fn modulo(v: u64) -> u64 {
        let v = (v & MOD) + (v >> 61);
        if v >= MOD {
            v - MOD
        } else {
            v
        }
    }
}

// 以下はmain()内に記述
let mut rng = rand::thread_rng();
let BASE = rng.gen_range(2,(1<<61)-1);
let rh = rolling_hash::RollingHash::new(&S.as_bytes(),BASE);

#[fastout]
fn main() {
    input! {
        N:usize,
        Q:usize,
        S:String,
        query:[(Usize1,Usize1,Usize1,Usize1);Q]
    }

    let mut rng = rand::thread_rng();
    let BASE = rng.gen_range(2,(1<<61)-1);
    let rh = rolling_hash::RollingHash::new(&S.as_bytes(),BASE);

    for &(a,b,c,d) in &query{
        if rh.get_hash(a, b+1) == rh.get_hash(c, d+1) {
            println!("Yes");
        }else{
            println!("No");
        }
    }
}
