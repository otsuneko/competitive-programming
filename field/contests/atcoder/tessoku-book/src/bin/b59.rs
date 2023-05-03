#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: usize = 1 << 60;

// 拝借元　https://github.com/kenkoooo/competitive-programming-rs/blob/master/src/data_structure/fenwick_tree.rs
pub mod fenwick_tree {
    /// `FenwickTree` is a data structure that can efficiently update elements
    /// and calculate prefix sums in a table of numbers.
    /// [https://en.wikipedia.org/wiki/Fenwick_tree](https://en.wikipedia.org/wiki/Fenwick_tree)
    pub struct FenwickTree<T, F> {
        n: usize,
        data: Vec<T>,
        initialize: F,
    }

    impl<T, F> FenwickTree<T, F>
    where
        T: Copy + std::ops::AddAssign + std::ops::Sub<Output = T>,
        F: Fn() -> T,
    {
        /// Constructs a new `FenwickTree`. The size of `FenwickTree` should be specified by `size`.
        pub fn new(size: usize, initialize: F) -> FenwickTree<T, F> {
            FenwickTree {
                n: size + 1,
                data: vec![initialize(); size + 1],
                initialize,
            }
        }

        pub fn add(&mut self, k: usize, value: T) {
            let mut x = k;
            while x < self.n {
                self.data[x] += value;
                x |= x + 1;
            }
        }

        /// Returns a sum of range `[l, r)`
        pub fn sum(&self, l: usize, r: usize) -> T {
            self.sum_one(r) - self.sum_one(l)
        }

        /// Returns a sum of range `[0, k)`
        pub fn sum_one(&self, k: usize) -> T {
            assert!(k < self.n, "Cannot calculate for range [{}, {})", k, self.n);
            let mut result = (self.initialize)();
            let mut x = k as i32 - 1;
            while x >= 0 {
                result += self.data[x as usize];
                x = (x & (x + 1)) - 1;
            }

            result
        }
    }
}

#[fastout]
fn main() {
    input! {
        N:usize,
        A:[usize;N]
    }

    let mut ans = 0;
    let mut BIT = fenwick_tree::FenwickTree::new(N, || 0);
    for i in 0..N{
        ans += i - BIT.sum_one(A[i]);
        BIT.add(A[i], 1);
    }

    println!("{}",ans);
}
