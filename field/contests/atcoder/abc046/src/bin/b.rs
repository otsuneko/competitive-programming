use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        N:usize,
        K:usize
    }

    let mut ans:usize = K;

    for _i in 0..N-1{
        ans *= K-1;
    }

    println!("{}",ans);

}
