use proconio::{fastout, input};
use num::abs;
use nalgebra::min;

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        N:i64,
        A:[i64;N]
    }

    let total = A.iter().sum::<i64>();

    let mut mi = 10_i64.pow(12);
    let mut su = 0;

    for a in A{
        su += a;
        mi = min(mi,abs(total-su-su))
    }

    println!("{}",mi);

}