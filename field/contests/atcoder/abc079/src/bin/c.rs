use proconio::{fastout, input, marker::Chars};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        kippu:Chars
    }

    for bit in 0..(1<<3){
        let mut su:i32 = kippu[0].to_digit(10).unwrap() as i32;
        let mut ans:String = kippu[0].to_string();

        for i in 0..3{
            if bit & (1<<i) > 0{
                su += kippu[i+1].to_digit(10).unwrap() as i32;
                ans = ans + "+" + &kippu[i+1].to_string();
            }else{
                su -= kippu[i+1].to_digit(10).unwrap() as i32;
                ans = ans + "-" + &kippu[i+1].to_string();
            }
        }

        if su == 7{
            println!("{}=7",ans);
            break
        }
    }
}
