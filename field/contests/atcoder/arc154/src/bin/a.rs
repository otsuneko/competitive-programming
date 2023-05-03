// -*- coding:utf-8-unix -*-
// #![feature(map_first_last)]
#![allow(dead_code)]
#![allow(unused_imports)]
#![allow(unused_macros)]
use core::num;
use std::cmp::*;
use std::fmt::*;
use std::hash::*;
use std::*;
use std::{cmp, collections, fmt, io, iter, ops, str};
const INF: i64 = 1223372036854775807;
const UINF: usize = INF as usize;
const LINF: i64 = 2147483647;
const INF128: i128 = 1223372036854775807000000000000;
// const MOD: i64 = 1000000007;
const MOD: i64 = 998244353;
const UMOD: usize = MOD as usize;
const M_PI: f64 = 3.14159265358979323846;
// const MOD: i64 = INF;
 
use cmp::Ordering::*;
use std::collections::*;
use std::io::stdin;
use std::io::stdout;
use std::io::Write;

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
    pub n: i64,
    pub buf: Vec<M::T>,
}

impl<M: Monoid> SEG<M> {
    pub fn new(n: i64) -> SEG<M> {
        let mut m = 1;
        while m < n { m *= 2; }
        SEG {
            n: m,
            buf: vec![M::id().clone(); 2 * m as usize],
        }
    }

    pub fn update(&mut self, k: i64, a: M::T) {
        let mut k = k + self.n as i64;
        self.buf[k as usize] = a;

        while k > 1 {
            k = k >> 1;
            self.buf[k as usize] = M::op(&self.buf[k as usize*2], &self.buf[k as usize*2+1]);
        }
    }
    
    pub fn get(&self, k: usize) -> M::T {
        self.buf[k + self.n as usize].clone()
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
        self.do_query(a,b,1,0,self.n as usize)
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

pub fn digsum(mut n:usize) -> usize{
    let mut res = 0;
    while n > 0{
        res += n%10;
        n /= 10;
    }
    return res
}

#[allow(dead_code)]
fn read<T: std::str::FromStr>() -> T {
    let mut s = String::new();
    std::io::stdin().read_line(&mut s).ok();
    s.trim().parse().ok().unwrap()
}
 
#[allow(dead_code)]
fn read_vec<T: std::str::FromStr>() -> Vec<T> {
    read::<String>()
        .split_whitespace()
        .map(|e| e.parse().ok().unwrap())
        .collect()
}


fn main() {
    let T: usize = read();

    for _ in 0..T{
        let tmp:Vec<usize> = read_vec();
        let N:usize = tmp[0];
        let Q:usize = tmp[1];
        let mut A:Vec<usize> = read_vec();
        
        let mut cnt = HashMap::<usize,usize>::new();
        for i in 0..N{
            cnt.entry(i).or_insert(0);
        }

        let mut seg = SEG::<SUM>::new(N as i64 + 1);

        for _ in 0..Q{
            let mut query:Vec<usize> = read_vec();
            if query[0] == 1{
                query[1] -= 1;
                seg.update(query[1] as i64,seg.get(query[1])+1);
                seg.update(query[2] as i64,seg.get(query[2])-1);
            }else if query[0] == 2{
                let mut x = query[1];
                x -= 1;
                let mut num = seg.query(0,x+1) as usize - cnt.get(&x).unwrap();
                for _ in 0..num{
                    A[x] = digsum(A[x]);
                }
                cnt.entry(x).or_insert(seg.query(0,x+1) as usize);
                println!("{}",A[x]);
            }
        }
    }
}
