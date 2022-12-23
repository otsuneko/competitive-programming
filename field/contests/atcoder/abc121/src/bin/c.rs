use proconio::{fastout, input};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        N:usize,
        M:usize,
        mut drink:[[usize;2];N]
    }

    drink.sort();
    // println!("{}",drink.iter().map(|x| x.iter().join(" ")).join("\n"));
    let mut cnt = 0;
    let mut ans = 0;

    for v in drink{
        let (a,b) = (v[0],v[1]);
        if cnt+b < M{
            cnt += b;
            ans += a*b;
        }else{
            ans += a*(M-cnt);
            break;
        }
    }

    println!("{}",ans);
}
