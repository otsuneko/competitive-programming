use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        N:usize
    }

    let mut ans = 1;
    for i in 1..N+1{
        ans = ans*i%(10_usize.pow(9)+7);
    }

    println!("{}",ans);
}
