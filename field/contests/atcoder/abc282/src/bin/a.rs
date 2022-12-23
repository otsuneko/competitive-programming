use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        K:usize
    }

    let alpha: String = (b'A'..=b'Z').map(char::from).collect();

    println!("{}",&alpha[..K]);
}
