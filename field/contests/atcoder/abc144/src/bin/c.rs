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

// #[allow(non_snake_case)]
// fn bfs(n: usize) -> usize{
//     let mut queue = VecDeque::new();
//     queue.push_back((1,1,0));

//     let MOVE = [(0,1),(1,0)];
//     while !queue.is_empty(){
//         let (y,x,cnt) = queue.pop_front().unwrap();
//         if y*x == n{
//             return cnt;
//         }

//         for (dy,dx) in &MOVE{
//             queue.push_back((y+dy,x+dx,cnt+1));
//         }
//     }
//     return 0
// }

// fn is_prime(n: usize) -> bool {
//     n != 1 && (2..).take_while(|i| i*i <= n).all(|i| n%i != 0)
// }

#[fastout]
#[allow(non_snake_case, non_upper_case_globals, path_statements)]
fn main() {
    input! {
        N:usize
    }

    let mut ans = N-1;
    for i in 2..=10usize.pow(6){
        if N%i == 0{
            ans = min(ans, i-1 + N/i-1)
        }
    }

    println!("{}",ans);
}
