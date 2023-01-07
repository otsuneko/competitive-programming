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

fn divisor(n:usize) -> Vec<usize>{
    let mut res = vec![];
    for i in (1..).take_while(|x| x*x <= n){
        if n%i == 0{
            res.push(i);
            if i*i != n{
                res.push(n/i);
            }
        }
    }
    res.sort();
    return res;
}

fn is_prime(n: i64) -> bool {
    n != 1 && (2..).take_while(|i| i*i <= n).all(|i| n%i != 0)
  }

fn prime_decomposition(mut n:usize) -> Vec<usize> {
    let mut i = 2;
    let mut table = vec![];
    while i*i <= n{
        while n%i == 0{
            n /= i;
            table.push(i);
        }
        i += 1;
    }
    if n > 1{
        table.push(n);
    }
    return table;
}

#[fastout]
#[allow(non_snake_case, non_upper_case_globals, path_statements)]
fn main() {
    input! {
        N:usize,
        A:[usize;N]
    }

    let mut ans = 0;
    for a in &A{
        ans += a.trailing_zeros();
    }
    println!("{}",ans);

}
