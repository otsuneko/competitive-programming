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
        N:usize,
        S:[String;N],
        M:usize,
        T:[String;M]
    }

    let mut mp_s = HashMap::new();
    let mut mp_t = HashMap::new();

    for s in S{
        *mp_s.entry(s).or_insert(0) += 1;
    }

    for t in T{
        *mp_t.entry(t).or_insert(0) += 1;
    }

    let mut ans = 0;
    for (k,v) in mp_s{
        ans = max(ans, v - mp_t.get(&k).unwrap_or(&0));
    }

    println!("{}",ans);

}
