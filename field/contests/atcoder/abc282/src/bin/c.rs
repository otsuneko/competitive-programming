use proconio::{fastout, input, marker::Chars};
use itertools::*;

#[fastout]
#[allow(non_snake_case, non_upper_case_globals, dead_code)]
fn main() {
    input! {
        _N: i32,
        mut S: Chars
    }

    let mut c = 0;
    for s in S.iter_mut(){
        if *s == '"'{
            c ^= 1;
        }else if (*s,c) == (',', 0){
            *s = '.';
        }
    }

    println!("{}",S.iter().join(""));

}
