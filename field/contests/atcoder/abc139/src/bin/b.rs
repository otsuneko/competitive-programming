use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        A:f32,
        B:f32
    }

    println!("{}",((B-1.0)/(A-1.0)).ceil());
}
