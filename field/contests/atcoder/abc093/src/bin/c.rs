use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        mut num:[usize;3]
    }

    num.sort();

    let mut ans = 0;

    while num[1] < num[2]{
        num[0] += 1;
        num[1] += 1;
        ans += 1
    }

    if (num[1]-num[0])%2 == 0{
        ans += (num[1]-num[0])/2;
    }else{
        ans += (num[1]+1-num[0])/2 + 1;
    }

    println!("{}",ans);
}
