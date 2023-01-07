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
        A:usize,
        B:usize
    }

    if (B-A)%2 == 0{
        println!("{}",(B-A)/2);
    }else{
        if B > N-A{
            let mut ans = N-B;
            let B2 = N;
            let A2 = A+ans;
            ans += (B2-A2+1)/2;
            println!("{}",ans);
        }else{
            let mut ans = A;
            let A2 = 1;
            let B2 = B-ans;
            ans += (B2-A2+1)/2;
            println!("{}",ans);
        }

    }
}
