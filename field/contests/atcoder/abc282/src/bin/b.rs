use proconio::{fastout, input, marker::Bytes};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        N: usize,
        M: usize,
        S: [Bytes;N]
    }

    let mut ans: i32 = 0;

    for i in 0..N{
        for j in i+1..N{
            let mut flag:bool = true;
            for k in 0..M{
                flag &= S[i][k] == b'o' || S[j][k] == b'o';
                // if S[i].chars().nth(k) == Some('x') && S[j].chars().nth(k) == Some('x'){
                //     flag = false;
                // }
            }
            if flag {
                ans += 1;
            }
        }
    }

    println!("{}",ans);
}
