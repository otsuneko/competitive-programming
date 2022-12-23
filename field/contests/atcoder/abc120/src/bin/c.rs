use proconio::{fastout, input, marker::Chars};

#[fastout]
#[allow(non_snake_case, non_upper_case_globals)]
fn main() {
    input! {
        S:Chars
    }

    let mut vec:Vec<char> = Vec::new();

    for i in 0..S.len(){
        if vec.len() > 0 && vec[vec.len()-1] != S[i]{
            vec.pop();
        }else{
            vec.push(S[i]);
        }
    }

    println!("{}",S.len()-vec.len());


}
