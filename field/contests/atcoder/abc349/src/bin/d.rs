#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;
use rustc_hash::FxHashMap;

const INF: usize = 1 << 60;

/// https://github.com/akiradeveloper/rust-comp-snippets/blob/master/src/seg.rs
/// フェニック木の一般化
/// 各ノードには最初、idに相当する値が入っている。
/// let mut seg:SEG<SUM> = SEG::new(N);
/// get i: a[i]を返す
/// update i x: a[i]=x
/// query l r: [l,r)をカバーするノードに対してopを適用したもの

pub trait Monoid {
    type T: Clone + std::fmt::Debug;
    fn id() -> Self::T;
    fn op(a: &Self::T, b: &Self::T) -> Self::T;
}

pub struct SEG<M: Monoid> {
    pub n: usize,
    pub buf: Vec<M::T>,
}

impl<M: Monoid> SEG<M> {
    pub fn new(n: usize) -> SEG<M> {
        let mut m = 1;
        while m < n { m *= 2; }
        SEG {
            n: m,
            buf: vec![M::id().clone(); 2 * m],
        }
    }

    pub fn update(&mut self, k: usize, a: M::T) {
        let mut k = k + self.n;
        self.buf[k] = a;

        while k > 1 {
            k = k >> 1;
            self.buf[k] = M::op(&self.buf[k*2], &self.buf[k*2+1]);
        }
    }

    pub fn get(&self, k: usize) -> M::T {
        self.buf[k + self.n].clone()
    }

    pub fn do_query(&self, a: usize, b: usize, k: usize, l: usize, r: usize) -> M::T {
        if r <= a || b <= l {
            return M::id();
        }

        if a <= l && r <= b {
            return self.buf[k].clone();
        } else {
            let vl = self.do_query(a,b,k*2,l,(l+r)/2);
            let vr = self.do_query(a,b,k*2+1,(l+r)/2,r);
            return M::op(&vl, &vr);
        }
    }

    // [a,b)
    pub fn query(&self, a: usize, b: usize) -> M::T {
        self.do_query(a,b,1,0,self.n)
    }
}

struct SUM;
impl Monoid for SUM {
    type T = i64;
    fn id() -> Self::T {
        0
    }
    fn op(a: &Self::T, b: &Self::T) -> Self::T {
        *a + *b
    }
}

struct MAX;
impl Monoid for MAX {
    type T = i64;
    fn id() -> Self::T {
        std::i64::MIN
    }
    fn op(a: &Self::T, b: &Self::T) -> Self::T {
        max(*a, *b)
    }
}

#[fastout]
fn main() {
    input! {
        mut L: usize,
        mut R: usize,
    }

    let mut ans = vec![];
    while L != R {
        let mut i = 0;
        while L % 2_usize.pow(i+1) == 0 && L+2_usize.pow(i+1) <= R {
            i += 1;
        }
        ans.push((L, L+2_usize.pow(i)));
        L += 2_usize.pow(i);
    }

    println!("{}", ans.len());
    for (l,r) in ans {
        println!("{} {}", l, r);
    }

}
