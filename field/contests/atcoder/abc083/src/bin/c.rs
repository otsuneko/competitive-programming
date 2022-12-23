use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        X:usize,
        Y:usize
    }

    let mut ans = 0;
    let mut n = X;

    while n <= Y {
        n *= 2;
        ans += 1;
    }

    println!("{}",ans);
}
