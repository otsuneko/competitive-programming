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
        S:Chars,
    }

    let mut used: HashSet<char> = HashSet::new();
    let mut stack:Vec<char> = Vec::new();

    for i in 0..S.len(){
        if S[i] == ')'{
            loop{
                let c = stack.pop().unwrap();
                if c == '('{
                    break
                }else{
                    used.remove(&c);
                }
            }
        }else{
            stack.push(S[i]);
            if S[i] != '('{
                if used.contains(&S[i]){
                    println!("No");
                    return
                }
                used.insert(S[i]);
            }
        }
    }

    println!("Yes");

}
