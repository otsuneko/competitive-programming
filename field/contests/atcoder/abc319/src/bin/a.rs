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

const INF: usize = 1 << 60;


#[fastout]
fn main() {
    input! {S:String}
    let mut players = HashMap::new();
    players.insert("tourist",3858);
    players.insert("ksun48",3679);
    players.insert("Benq",3658);
    players.insert("Um_nik",3648);
    players.insert("apiad",3638);
    players.insert("Stonefeang",3630);
    players.insert("ecnerwala",3613);
    players.insert("mnbvmar",3555);
    players.insert("newbiedmy",3516);
    players.insert("semiexp",3481);

    if let Some(score) = players.get(&S[..]) {
        println!("{}", score);
    } else {
        println!("Player not found");
    }
    
}
