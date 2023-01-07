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
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        S:Chars
    }

    let mut ans = 0;
    let mut idx = 0;
    while idx < S.len(){
        if S[idx] == '0'{
            if idx < S.len()-1 && S[idx+1] == '0'{
                ans += 1;
                idx += 2;
            }else{
                ans += 1;
                idx += 1;
            }
        }else{
            ans += 1;
            idx += 1;
        }
    }

    println!("{}",ans);
}
