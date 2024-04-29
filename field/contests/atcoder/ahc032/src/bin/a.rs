#![allow(non_snake_case)]
use proconio::{input, source::once::OnceSource};
use itertools::*;

// const TIMELIMIT: u64 = 1900;
const N: usize = 9;
const M: usize = 20;
const K: usize = 81;
const MOD: u64 = 998244353;

struct Input {
    a: [[u64; N]; N],
    s: [[[u64; 3]; 3]; M],
}

fn read_input<R: std::io::BufRead>(reader: R) -> Input {
    let source = OnceSource::new(reader);
    input!{
        from source,
        _n: usize,
        _m: usize,
        _k: usize,
        a1: [[u64; N]; N],
        s1: [[[u64; 3]; 3]; M],
    }
    let mut a = [[0; N]; N];
    let mut s = [[[0; 3]; 3]; M];
    for i in 0..N { for j in 0..N { a[i][j] = a1[i][j]; } }
    for k in 0..M { for i in 0..3 { for j in 0..3 { s[k][i][j] = s1[k][i][j]; } } }
    Input {a, s}
}

fn read_input_from_stdin() -> Input {
    read_input(std::io::BufReader::new(std::io::stdin()))
}

fn read_input_from_file(f: &std::fs::File) -> Input {
    read_input(std::io::BufReader::new(f))
}

type Answer = Vec<(usize, usize, usize)>;

fn write_output(out: &Answer) {
    println!("{}", out.len());
    for (m, p, q) in out {
        println!("{m} {p} {q}");
    }
}

fn calc_score(input: &Input, ans: &Answer) -> i64 {
    let mut b = input.a.clone();
    for (m, p, q) in ans {
        apply(&mut b, *p, *q, &input.s[*m])
    }
    b.iter().map(|row| row.iter().sum::<u64>()).sum::<u64>() as i64
}

fn apply(a: &mut [[u64; N]; N], p: usize, q: usize, stamp: &[[u64; 3]; 3]) {
    for i in 0..3 {
        for j in 0..3 {
            a[p + i][q + j] += stamp[i][j];
            if a[p + i][q + j] >= MOD {
                a[p + i][q + j] -= MOD;
            }
        }
    }
}

#[derive(Clone)]
struct State {
    a: [[u64; N]; N],
    ans: Answer,
    score: u64,
    progress: usize,
}

fn solve(input: &Input) -> Answer {
    // ビームサーチのqueue
    let mut q = Vec::new();
    q.push(State{a: input.a.clone(), ans: Vec::new(), score: 0, progress: 0});
    let beam_width = 3000;
    // stampを1~4回適用したときの変化量を全パターン分事前計算してs1,s2,s3,s4に格納
    let (s1, s2, s3, s4) = {
        let apply = |a: &mut [[u64; 3]; 3], s: &[[u64; 3]; 3]| {
            for i in 0..3 {
                for j in 0..3 {
                    a[i][j] += s[i][j];
                    if a[i][j] >= MOD { a[i][j] -= MOD; }
                }
            }
        };
        let unapply = |a: &mut [[u64; 3]; 3], s: &[[u64; 3]; 3]| {
            for i in 0..3 {
                for j in 0..3 {
                    if a[i][j] >= s[i][j] { a[i][j] -= s[i][j]; }
                    else { a[i][j] += MOD - s[i][j]; }
                }
            }
        };
        let mut s1 = Vec::new();
        let mut s2 = Vec::new();
        let mut s3 = Vec::new();
        let mut s4 = Vec::new();
        let mut a = [[0; 3]; 3];
        for m1 in 0..M {
            apply(&mut a, &input.s[m1]);
            s1.push((m1, a.clone()));
            for m2 in m1..M {
                apply(&mut a, &input.s[m2]);
                s2.push((m1, m2, a.clone()));
                for m3 in m2..M {
                    apply(&mut a, &input.s[m3]);
                    s3.push((m1, m2, m3, a.clone()));
                    for m4 in m3..M {
                        apply(&mut a, &input.s[m4]);
                        s4.push((m1, m2, m3, m4, a.clone()));
                        unapply(&mut a, &input.s[m4]);
                    }
                    unapply(&mut a, &input.s[m3]);
                }
                unapply(&mut a, &input.s[m2]);
            }
            unapply(&mut a, &input.s[m1]);
        }
        (s1, s2, s3, s4)
    };
    // 各マスでのスタンプ適用可能回数のしきい値(しきい値を超えるとペナルティが発生する)
    let penalty_threshold: [usize; 49] = [
         2,  4,  6,  8, 10, 11, 12,
        15, 16, 17, 18, 19, 20, 21,
        24, 25, 26, 27, 28, 29, 30,
        33, 34, 35, 36, 37, 38, 39,
        42, 43, 44, 45, 46, 47, 48,
        51, 52, 53, 54, 55, 56, 57,
        60, 63, 67, 70, 73, 77, 81,
    ];

    let penalty_coefficient: u64 = 100_000_000;
    let calc_penalty = |p, len| {
        if len > penalty_threshold[p] {
            (len - penalty_threshold[p]) as u64 * penalty_coefficient
        } else {
            0
        }
    };

    // ビームサーチ
    for (i, j) in (0..=N-3).cartesian_product(0..=N-3) {
        let mut nextq = Vec::new();
        if i == N - 3 && j == N - 3 {
            while let Some(st) = q.pop() {
                let eval = |b: &[[u64; N]; N]| {
                    b[N-3][N-3..].iter().sum::<u64>() +
                        b[N-2][N-3..].iter().sum::<u64>() +
                        b[N-1][N-3..].iter().sum::<u64>()
                };

                let len = st.ans.len();
                if len > K {
                    continue;
                }

                let mut best_eval = eval(&st.a);
                let mut m = (None, None, None, None);

                if len + 1 <= K {
                    if let Some((m1, _, val)) = s1.iter().map(|(m1, s)| {
                        let mut b = st.a.clone();
                        apply(&mut b, N-3, N-3, &s);
                        (m1, s, eval(&b))
                    }).max_by_key(|(_, _, v)| *v)
                    {
                        if best_eval < val {
                            best_eval = val;
                            m = (Some(m1), None, None, None);
                        }
                    }
                }

                if len + 2 <= K {
                    if let Some((m1, m2, _, val)) = s2.iter().map(|(m1, m2, s)| {
                        let mut b = st.a.clone();
                        apply(&mut b, N-3, N-3, &s);
                        (m1, m2, s, eval(&b))
                    }).max_by_key(|(_, _, _, v)| *v)
                    {
                        if best_eval < val {
                            best_eval = val;
                            m = (Some(m1), Some(m2), None, None);
                        }
                    }
                }

                if len + 3 <= K {
                    if let Some((m1, m2, m3, _, val)) = s3.iter().map(|(m1, m2, m3, s)| {
                        let mut b = st.a.clone();
                        apply(&mut b, N-3, N-3, &s);
                        (m1, m2, m3, s, eval(&b))
                    }).max_by_key(|(_, _, _, _, v)| *v)
                    {
                        if best_eval < val {
                            best_eval = val;
                            m = (Some(m1), Some(m2), Some(m3), None);
                        }
                    }
                }

                if len + 4 <= K {
                    if let Some((m1, m2, m3, m4, _, val)) = s4.iter().map(|(m1, m2, m3, m4, s)| {
                        let mut b = st.a.clone();
                        apply(&mut b, N-3, N-3, &s);
                        (m1, m2, m3, m4, s, eval(&b))
                    }).max_by_key(|(_, _, _, _, _, v)| *v)
                    {
                        if best_eval < val {
                            // best_eval = val;
                            m = (Some(m1), Some(m2), Some(m3), Some(m4));
                        }
                    }
                }

                let mut new_st = State{
                    a: st.a,
                    ans: st.ans.clone(),
                    score: st.score,
                    progress: st.progress + 1
                };
                if let Some(&m1) = m.0 {
                    new_st.ans.push((m1, N-3, N-3));
                    apply(&mut new_st.a, N-3, N-3, &input.s[m1]);
                }
                if let Some(&m2) = m.1 {
                    new_st.ans.push((m2, N-3, N-3));
                    apply(&mut new_st.a, N-3, N-3, &input.s[m2]);
                }
                if let Some(&m3) = m.2 {
                    new_st.ans.push((m3, N-3, N-3));
                    apply(&mut new_st.a, N-3, N-3, &input.s[m3]);
                }
                if let Some(&m4) = m.3 {
                    new_st.ans.push((m4, N-3, N-3));
                    apply(&mut new_st.a, N-3, N-3, &input.s[m4]);
                }

                new_st.score += eval(&new_st.a);
                nextq.push(new_st);
            }
        } else if i == N - 3 {
            while let Some(st) = q.pop() {
                let eval = |b: &[[u64; N]; N]| {
                    b[N-3][j] + b[N-2][j] + b[N-1][j]
                };

                nextq.push(State{
                    a: st.a,
                    ans: st.ans.clone(),
                    score: st.score + eval(&st.a) - calc_penalty(st.progress + 1, st.ans.len()),
                    progress: st.progress + 1
                });

                if let Some((m1, _, val)) = s1.iter().map(|(m1, s)| {
                    let mut b = st.a.clone();
                    apply(&mut b, N-3, j, &s);
                    (m1, s, eval(&b))
                }).max_by_key(|(_, _, v)| *v)
                {
                    let mut new_st = State{
                        a: st.a,
                        ans: st.ans.clone(),
                        score: st.score + val - calc_penalty(st.progress + 1, st.ans.len()),
                        progress: st.progress + 1
                    };
                    new_st.ans.push((*m1, N-3, j));
                    apply(&mut new_st.a, N-3, j, &input.s[*m1]);
                    nextq.push(new_st);
                }

                if let Some((m1, m2, _, val)) = s2.iter().map(|(m1, m2, s)| {
                    let mut b = st.a.clone();
                    apply(&mut b, N-3, j, &s);
                    (m1, m2, s, eval(&b))
                }).max_by_key(|(_, _, _, v)| *v)
                {
                    let mut new_st = State{
                        a: st.a,
                        ans: st.ans.clone(),
                        score: st.score + val - calc_penalty(st.progress + 1, st.ans.len()),
                        progress: st.progress + 1
                    };
                    new_st.ans.push((*m1, N-3, j));
                    apply(&mut new_st.a, N-3, j, &input.s[*m1]);
                    new_st.ans.push((*m2, N-3, j));
                    apply(&mut new_st.a, N-3, j, &input.s[*m2]);
                    nextq.push(new_st);
                }


                if let Some((m1, m2, m3, _, val)) = s3.iter().map(|(m1, m2, m3, s)| {
                    let mut b = st.a.clone();
                    apply(&mut b, N-3, j, &s);
                    (m1, m2, m3, s, eval(&b))
                }).max_by_key(|(_, _, _, _, v)| *v)
                {
                    let mut new_st = State{
                        a: st.a,
                        ans: st.ans.clone(),
                        score: st.score + val - calc_penalty(st.progress + 1, st.ans.len()),
                        progress: st.progress + 1
                    };
                    new_st.ans.push((*m1, N-3, j));
                    apply(&mut new_st.a, N-3, j, &input.s[*m1]);
                    new_st.ans.push((*m2, N-3, j));
                    apply(&mut new_st.a, N-3, j, &input.s[*m2]);
                    new_st.ans.push((*m3, N-3, j));
                    apply(&mut new_st.a, N-3, j, &input.s[*m3]);
                    nextq.push(new_st);
                }
            }
        } if j == N - 3 {
            while let Some(st) = q.pop() {
                let eval = |b: &[[u64; N]; N]| {
                    b[i][N-3..].iter().sum::<u64>()
                };

                nextq.push(State{
                    a: st.a,
                    ans: st.ans.clone(),
                    score: st.score + eval(&st.a),
                    progress: st.progress + 1
                });

                if let Some((m1, val)) = s1.iter().map(|(m1, s)| {
                    let mut b = st.a.clone();
                    apply(&mut b, i, N-3, &s);
                    (m1, eval(&b))
                }).max_by_key(|(_, v)| *v)
                {
                    let mut new_st = State{
                        a: st.a,
                        ans: st.ans.clone(),
                        score: st.score + val - calc_penalty(st.progress + 1, st.ans.len()),
                        progress: st.progress + 1
                    };
                    new_st.ans.push((*m1, i, N-3));
                    apply(&mut new_st.a, i, N-3, &input.s[*m1]);
                    nextq.push(new_st);
                }

                if let Some((m1, m2, val)) = s2.iter().map(|(m1, m2, s)| {
                    let mut b = st.a.clone();
                    apply(&mut b, i, N-3, &s);
                    (m1, m2, eval(&b))
                }).max_by_key(|(_, _, v)| *v)
                {
                    let mut new_st = State{
                        a: st.a,
                        ans: st.ans.clone(),
                        score: st.score + val - calc_penalty(st.progress + 1, st.ans.len()),
                        progress: st.progress + 1
                    };
                    new_st.ans.push((*m1, i, N-3));
                    apply(&mut new_st.a, i, N-3, &input.s[*m1]);
                    new_st.ans.push((*m2, i, N-3));
                    apply(&mut new_st.a, i, N-3, &input.s[*m2]);
                    nextq.push(new_st);
                }


                if let Some((m1, m2, m3, val)) = s3.iter().map(|(m1, m2, m3, s)| {
                    let mut b = st.a.clone();
                    apply(&mut b, i, N-3, &s);
                    (m1, m2, m3, eval(&b))
                }).max_by_key(|(_, _, _, v)| *v)
                {
                    let mut new_st = State{
                        a: st.a,
                        ans: st.ans.clone(),
                        score: st.score + val - calc_penalty(st.progress + 1, st.ans.len()),
                        progress: st.progress + 1
                    };
                    new_st.ans.push((*m1, i, N-3));
                    apply(&mut new_st.a, i, N-3, &input.s[*m1]);
                    new_st.ans.push((*m2, i, N-3));
                    apply(&mut new_st.a, i, N-3, &input.s[*m2]);
                    new_st.ans.push((*m3, i, N-3));
                    apply(&mut new_st.a, i, N-3, &input.s[*m3]);
                    nextq.push(new_st);
                }
            }
        } else {
            while let Some(st) = q.pop() {
                let eval = |b: &[[u64; N]; N]| {
                    b[i][j]
                };

                nextq.push(State{
                    a: st.a,
                    ans: st.ans.clone(),
                    score: st.score + eval(&st.a) - calc_penalty(st.progress + 1, st.ans.len()),
                    progress: st.progress + 1
                });

                if let Some((m1, _, val)) = s1.iter().map(|(m1, s)| {
                    let mut b = st.a.clone();
                    apply(&mut b, i, j, &s);
                    (m1, s, eval(&b))
                }).max_by_key(|(_, _, v)| *v)
                {
                    let mut new_st = State{
                        a: st.a,
                        ans: st.ans.clone(),
                        score: st.score + val - calc_penalty(st.progress + 1, st.ans.len()),
                        progress: st.progress + 1
                    };
                    new_st.ans.push((*m1, i, j));
                    apply(&mut new_st.a, i, j, &input.s[*m1]);
                    nextq.push(new_st);
                }

                if let Some((m1, m2, _, val)) = s2.iter().map(|(m1, m2, s)| {
                    let mut b = st.a.clone();
                    apply(&mut b, i, j, &s);
                    (m1, m2, s, eval(&b))
                }).max_by_key(|(_, _, _, v)| *v)
                {
                    let mut new_st = State{
                        a: st.a,
                        ans: st.ans.clone(),
                        score: st.score + val - calc_penalty(st.progress + 1, st.ans.len()),
                        progress: st.progress + 1
                    };
                    new_st.ans.push((*m1, i, j));
                    apply(&mut new_st.a, i, j, &input.s[*m1]);
                    new_st.ans.push((*m2, i, j));
                    apply(&mut new_st.a, i, j, &input.s[*m2]);
                    nextq.push(new_st);
                }
            }
        }
        nextq.sort_by(|st1, st2| st2.score.cmp(&st1.score));
        let n = nextq.len().min(beam_width);
        q = nextq.into_iter().take(n).collect::<Vec<_>>();
        eprintln!("{} {}", q.len(), q[0].score);
    }

    eprintln!("{:?}", q[0].a);
    let ans = q[0].ans.clone();
    ans
}

fn main() {
    let input = {
        std::env::args().nth(1)
            .map(|file| std::fs::File::open(file).ok())
            .flatten()
            .map(|f| read_input_from_file(&f))
            .unwrap_or_else(|| read_input_from_stdin())
    };

    let out = solve(&input);
    write_output(&out);
    let score = calc_score(&input, &out);
    eprintln!("score = {score}");
}
