use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        N:i32,
        X:[i32;N]
    }

    let ans = (0..101).map(|p| X.iter().map(|&x_i| (x_i - p).pow(2)).sum::<i32>()).min().unwrap();

    println!("{}",ans);
}
