#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use itertools::Itertools;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    process::exit,
};

const INF: usize = 1 << 60;

// "q=deque()",
// "for c in a:",
// "    q.append(c)  ## dequeの右端に要素を一つ追加する。",
// "    (追加した要素に応じて何らかの処理を行う)",
// "",
// "    while not (満たすべき条件):",
// "        rm=q.popleft() ## 条件を満たさないのでdequeの左端から要素を取り除く",
// "        (取り除いた要素に応じて何らかの処理を行う)",
// "",
// "    (何らかの処理を行う。whileがbreakしたので、dequeに入っている連続部分列は条件を満たしている。特に右端の要素から左に延ばせる最大の長さになっている。)",

#[fastout]
fn main() {
    input! {
        N:usize,
        K:usize,
        A:[usize;N]
    }

    let mut ans = 0;

    let mut q:VecDeque<usize> = VecDeque::new();
    for &c in &A{
        q.push_back(c); //dequeの右端に要素を一つ追加する。
        //(追加した要素に応じて何らかの処理を行う)

        while !(q[q.len()-1]-q[0] <= K){
            let rm = q.pop_front().unwrap(); //条件を満たさないのでdequeの左端から要素を取り除く
            //(取り除いた要素に応じて何らかの処理を行う)
        }

        //(何らかの処理を行う。whileがbreakしたので、dequeに入っている連続部分列は条件を満たしている。特に右端の要素から左に延ばせる最大の長さになっている。)
        if q.len() >= 2{
            ans += q.len()-1;
        }
    }

    println!("{}",ans);
}
