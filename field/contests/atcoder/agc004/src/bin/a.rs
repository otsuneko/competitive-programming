use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        mut li:[usize;3]
    }

    li.sort();

    let ans = if li[2]%2==1 {li[1]*li[0]} else {0};

    println!("{}",ans);
}
