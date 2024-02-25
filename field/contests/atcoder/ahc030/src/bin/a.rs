#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use std::{
    cmp::{max, min, Reverse}, collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque}, io::{self, stdin, BufRead, BufReader, Write}, mem::swap, ops::{Add, Neg, Sub}, process::exit, time::Instant
};
use itertools::{iproduct, Itertools};
use superslice::Ext;
use proconio::{*, marker::*, source::line::LineSource};
const INF: usize = 1 << 60;

const INF_F64: f64 = 1e10;
const INF_I64: i64 = 1_000_000_000;
const MIN_POWER: usize = 0;
const MAX_POWER: usize = 1_000;
const MAX_MEASUREMENT: usize = 10_000;
// const MAX_MEASUREMENT: usize = 10;
const NEIGHBOR_SIZE: usize = 4;
const DIJ: [(usize, usize); NEIGHBOR_SIZE] = [(0, 1), (1, 0), (0, !0), (!0, 0)];


/// 現在時刻を返す
pub fn get_time() -> f64 {
    static mut STIME: f64 = -1.0;
    let t = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap();
    let ms = t.as_secs() as f64 + t.subsec_nanos() as f64 * 1e-9;
    unsafe {
        if STIME < 0.0 {
            STIME = ms;
        }
        #[cfg(feature = "local")]
        {
            (ms - STIME) * 1.5
        }
        #[cfg(not(feature = "local"))]
        {
            ms - STIME
        }
    }
}

/// 最小･最大の交換
/// A.chmax(B)のようにすることで，もしA<BならA=Bとしてtrueを返し，そうでなければAのまま保持してfalseを返す
pub trait ChangeMinMax {
    fn chmin(&mut self, x: Self) -> bool;
    fn chmax(&mut self, x: Self) -> bool;
}
impl<T: PartialOrd> ChangeMinMax for T {
    fn chmin(&mut self, x: Self) -> bool {
        *self > x && {
            *self = x;
            true
        }
    }
    fn chmax(&mut self, x: Self) -> bool {
        *self < x && {
            *self = x;
            true
        }
    }
}

#[derive(Debug, Clone, Copy)]
struct Edge {
    to: usize,
    cap: isize,
    cost: i64,
    rev: usize,
}
#[derive(Debug, Clone)]
struct MinCostFlow {
    n: usize,
    graph: Vec<Vec<Edge>>,
    h: Vec<i64>,
    dist: Vec<i64>,
    prev: Vec<(usize, usize)>,
}
impl MinCostFlow {
    fn new(n: usize) -> Self {
        MinCostFlow {
            n: n,
            graph: vec![vec![]; n],
            h: vec![0; n],
            dist: vec![0; n],
            prev: vec![(0, 0); n],
        }
    }
    fn add_edge(&mut self, from: usize, to: usize, cap: isize, cost: i64) {
        let fst = Edge {
            to: to,
            cap: cap,
            cost: cost,
            rev: self.graph[to].len(),
        };
        self.graph[from].push(fst);
        let snd = Edge {
            to: from,
            cap: 0,
            cost: -cost,
            rev: self.graph[from].len() - 1,
        };
        self.graph[to].push(snd);
    }
    fn min_cost_flow(&mut self, s: usize, t: usize, mut f: isize) -> i64 {
        let n = self.n;
        let inf: i64 = std::i64::MAX / 10;
        let mut res = 0;
        let h = &mut self.h;
        let dist = &mut self.dist;
        while f > 0 {
            let mut que = std::collections::BinaryHeap::<(i64, usize)>::new();
            for i in 0..n {
                dist[i] = inf;
            }
            dist[s] = 0;
            que.push((0, s));
            while let Some((d, v)) = que.pop() {
                let d = -d;
                if dist[v] < d {
                    continue;
                }
                for (i, &e) in self.graph[v].iter().enumerate() {
                    if e.cap > 0 && dist[e.to] > dist[v] + e.cost + h[v] - h[e.to] {
                        dist[e.to] = dist[v] + e.cost + h[v] - h[e.to];
                        self.prev[e.to] = (v, i);
                        que.push((-dist[e.to], e.to));
                    }
                }
            }
            if dist[t] == inf {
                return -1;
            }
            for i in 0..n {
                h[i] += dist[i];
            }
            let mut d = f;
            let mut i = t;
            while i != s {
                let (pv, pe) = self.prev[i];
                d = std::cmp::min(d, self.graph[pv][pe].cap);
                i = pv;
            }
            f -= d;
            res += d as i64 * h[t];
            i = t;
            while i != s {
                let (pv, pe) = self.prev[i];
                self.graph[pv][pe].cap -= d;
                let erev = self.graph[pv][pe].rev;
                self.graph[i][erev].cap += d;
                i = pv;
            }
        }
        return res;
    }
}



// #[derive(Debug, Clone)]
// struct State {
//     high_temperature_point: Coordinate, // 高温地点
//     P: Vec<Vec<usize>>, // Another Spaceの温度
//     measure_count: usize, // 計測回数
//     probalility_table: Vec<Vec<f64>>, // ワームホールiが出口セルjである確率
//     correspondence: Vec<usize>, // ワームホールと出口セルの対応関係
// }
// impl State {
//     fn new(input: &Input) -> Self {
//         let mut high_temperature_point = Coordinate::new(!0, !0);
//         let mut min_dist = usize::MAX;
//         // Another Space上の各地点(y,x)のうち，全ての出口セルへのユークリッド距離の総和が最小の点を高温点にする
//         for y in 0..input.L {
//             for x in 0..input.L {
//                 let crt_coord = Coordinate::new(y, x);
//                 let mut dist = vec![0; input.N];
//                 for (i, &exit_coord) in input.exit_cells.iter().enumerate() {
//                     // トーラスであることを考慮された距離にする必要があることに注意
//                     dist[i] = crt_coord.manhattan_dist_with_torus(&exit_coord, input.L);
//                 }
//                 // 近い順に重みを付けた和にする
//                 dist.sort_unstable();
//                 let mut dist_sum = 0;
//                 for i in 0..input.N {
//                     dist_sum += dist[i] * (input.N - i);
//                 }
//                 if min_dist.chmin(dist_sum) {
//                     high_temperature_point = crt_coord;
//                 }
//             }
//         }
//         Self {
//             high_temperature_point,
//             P: vec![vec![0; input.L]; input.L],
//             measure_count: 0,
//             probalility_table: vec![vec![1.0 / input.N as f64; input.N]; input.N], // 各ワームホールと出口セルが確率1/Nで対応しているとする (無事前情報分布を使用するということ)
//             correspondence: vec![!0; input.N],
//         }
//     }

//     fn calc_relative_pos(&mut oil:Oil) {
//         let base_y = oil.pos_list[0].0;
//         let base_x = oil.pos_list[0].1;
        
//         oil.relative_pos_list = oil
//             .pos_list
//             .iter()
//             .map(|&(y, x)| (y - base_y, x - base_x))
//             .collect();
//     }

//     // 高温地帯からなだらかに山を作る
//     // ゆうさんの記事
//     // https://yuusanlondon.hatenablog.com/entry/2023/08/23/085128#fn-b1054056
//     fn init_power(&mut self, input: &Input) {
//         let diff = (MAX_POWER / 2).min((150).max(input.S * 3));
//         for y in 0..input.L {
//             for x in 0..input.L {
//                 if y == self.high_temperature_point.y && x == self.high_temperature_point.x {
//                     self.P[y][x] = MAX_POWER / 2 + diff;
//                 } else {
//                     self.P[y][x] = MAX_POWER / 2 - diff;
//                 }
//             }
//         }
//         // 十分な回数ループを回し，あるセルがその周囲4つのセルの平均値になるようにしたい
//         for _ in 0..1_000 {
//             let prev_p = self.P.clone();
//             for y in 0..input.L {
//                 for x in 0..input.L {
//                     let crt_coord = Coordinate::new(y, x);
//                     let dist = crt_coord.manhattan_dist_with_torus(&self.high_temperature_point, input.L);
//                     if 0 < dist && dist <= input.L / 2 {
//                         // [ToDo] このif文なんで？
//                         self.P[y][x] = {
//                             let mut mean = 0;
//                             for &(dy, dx) in &DIJ {
//                                 let neigh_y = (y + input.L + dy) % input.L;
//                                 let neigh_x = (x + input.L + dx) % input.L;
//                                 mean += prev_p[neigh_y][neigh_x];
//                             }
//                             (mean as f64 / 4.0).round() as usize
//                         };
//                     }
//                 }
//             }
//         }
//         for y in 0..input.L {
//             for x in 0..input.L {
//                 print!("{} ", self.P[y][x]);
//             }
//             println!();
//         }
//     }
//     // あるワームホールに対応する最尤の出口セルから高温点の方向に向かった計測の実行
//     // 実行回数上限を超えると !0 を返す
//     fn measure(&mut self, mut source: &mut LineSource<impl BufRead>, input: &Input, warmhole_idx: usize, exit_cell: Coordinate) -> usize {
//         if self.measure_count == MAX_MEASUREMENT {return !0;}
//         self.measure_count += 1;

//         // 高温点への距離をトーラスを考慮し，[-L/2, L/2]で表現する
//         let mut diff_y = ((self.high_temperature_point.y + input.L - exit_cell.y) % input.L) as isize;
//         let mut diff_x = ((self.high_temperature_point.x + input.L - exit_cell.x) % input.L) as isize;
//         // L/2より大きいなら逆から行ったほうがいい
//         if diff_y > input.L as isize / 2 {
//             diff_y -= input.L as isize
//         }
//         if diff_x > input.L as isize / 2 {
//             diff_x -= input.L as isize
//         }

//         println!("{} {} {}", warmhole_idx, diff_y, diff_x);
//         input! {
//             from &mut source,
//             m: usize
//         }

//         m
//     }
//     #[inline]
//     fn cdf(&self, x: f64, s: f64) -> f64 {
//         0.5 * (1.0 + libm::erf(x / (2.0 * s * s).sqrt()))
//     }
//     #[inline]
//     fn likelihood(&self, x_ob: usize, x_gt: usize, s: usize) -> f64 {
//         // 例えば，誤差が3なら，四捨五入を考えて[2.5, 3.5]の間に値が収まっている確率を知りたい
//         if x_ob == MIN_POWER {
//             // 観測が0のとき，標準偏差が大きいので誤差が[-∞, x_ob - x_gt]に収まる確率とする
//             self.cdf(x_ob as f64 - x_gt as f64 + 0.5, s as f64) - self.cdf(f64::NEG_INFINITY, s as f64)
//         } else if x_ob == MAX_POWER {
//             self.cdf(f64::INFINITY, s as f64) - self.cdf(x_ob as f64 - x_gt as f64 - 0.5, s as f64)
//         } else {
//             self.cdf(x_ob as f64 - x_gt as f64 + 0.5, s as f64) - self.cdf(x_ob as f64 - x_gt as f64 - 0.5, s as f64)
//         }
//     }
//     #[inline]
//     fn normalize_prob(mut v: &mut [f64]) {
//         let sum = v.iter().sum::<f64>();
//         for i in 0..v.len() {
//             v[i] /= sum;
//         }
//     }
//     // ベイズ推定により，あるワームホールと出口セルの対応の確率テーブルを作る
//     fn estimate(&mut self, mut source: &mut LineSource<impl BufRead>, input: &Input, warmhole_idx: usize, exit_cell: Coordinate) -> bool {
//         // このワームホールと対応する最尤の出口セルが実際に繋がっていると仮定する
//         // その出口セルから出て高温点の方向に向かったと時に，本当に高温なら実際に対応している確率が高くなる
//         // 逆に高温でないなら，対応していないとしたい
//         // 累積分布関数を使って，誤差がx未満になる確率を計算しつつ，ベイズの定理で更新していく
//         let m = self.measure(&mut source, &input, warmhole_idx, exit_cell);
//         if m == !0 {return false;}

//         let mut estimated_prob = vec![];
//         let diff_to_high_temp_y = (self.high_temperature_point.y + input.L - exit_cell.y) % input.L;
//         let diff_to_high_temp_x = (self.high_temperature_point.x + input.L - exit_cell.x) % input.L;
//         for &e_c in &input.exit_cells {
//             let ground_truth_y = (diff_to_high_temp_y + input.L + e_c.y) % input.L;
//             let ground_truth_x = (diff_to_high_temp_x + input.L + e_c.x) % input.L;
//             let ground_truth = self.P[ground_truth_y][ground_truth_x];

//             // cdfで誤差がm - ground_truth未満になる確率を計算する
//             let likelihood = self.likelihood(m, ground_truth, input.S);
//             estimated_prob.push(likelihood);
//         }

//         Self::normalize_prob(&mut estimated_prob);

//         // 確率テーブルを更新する        
//         for exit_cell_idx in 0..input.N {
//             // 今見ているwarmhole_idxがexit_cell_idxと対応している尤度をかける
//             self.probalility_table[warmhole_idx][exit_cell_idx] *= estimated_prob[exit_cell_idx];
//             // 今見ているwarmhole_idx以外がexit_cell_idxと対応していない尤度をかける
//             let estimated_inv_prob = (1.0 - estimated_prob[exit_cell_idx]) / (input.N - 1) as f64;
//             for warmhole_idx_2 in 0..input.N {
//                 if warmhole_idx != warmhole_idx_2 {
//                     self.probalility_table[warmhole_idx_2][exit_cell_idx] *= estimated_inv_prob;
//                 }
//             }
//         }
        
//         true
//     }
//     fn solve(&mut self, mut source: &mut LineSource<impl BufRead>, input: &Input) {
//         const THRESHOLD: f64 = 0.99;
//         // 行の最大値が閾値を超えるまで繰り返す
//         'main: for _ in 0..MAX_MEASUREMENT {
//             // estimateが走る行があったらtrueに
//             let mut flag = false;
//             for warmhole_idx in 0..input.N {
//                 // 一番尤度の高い出口セルを全探索で見つける
//                 let (likely_exit_cell_idx, max_prob) = self.probalility_table[warmhole_idx]
//                     .iter()
//                     .enumerate()
//                     .max_by(|&a, &b| a.1.partial_cmp(b.1).unwrap())
//                     .map(|(i, &v)| (i, v))
//                     .unwrap();
//                 // maxが閾値を超えてたらこのwarmhole_idxの最尤の出口セルがexit_cell_idxでほぼ確定しているので見なくてよい
//                 if max_prob >= THRESHOLD {continue;}
//                 // 更新が行われたことを管理
//                 flag = true;
//                 // warmhole_idxと最尤のexit_cell_idxが対応している確率と，他のwarmholeが対応していない確率を更新する
//                 // warmholeの計測回数が上限に到達したら外側のfor文を抜ける
//                 if !self.estimate(&mut source, &input, warmhole_idx, input.exit_cells[likely_exit_cell_idx]) {break 'main;}
//                 // 確率テーブルを正規化する
//                 for i in 0..input.N {
//                     Self::normalize_prob(&mut self.probalility_table[i]);
//                 }
//             }
//             // 全て更新されなくなったら修了
//             if !flag {break;}
//         }
//         // eprintln!("{:?}", self.p_table);
//     }
//     // 最小費用流でワームホールと出口セルとの完全マッチングを決める
//     fn detect_correspondence(&mut self, input: &Input) {
//         // ワームホールxN，出口セルxN，s/tの計2N+2個の頂点が必要
//         let mut mcf = MinCostFlow::new(input.N * 2 + 2);
//         // s: 2n, t: 2n+1とする
//         for i in 0..input.N {
//             // s->ワームホール
//             mcf.add_edge(input.N * 2, i, 1, 0);
//             // 出口セル->t
//             mcf.add_edge(i + input.N, input.N * 2 + 1, 1, 0);
//             // ワームホール->出口セル
//             for j in 0..input.N {
//                 // mcf.add_edge(i, j + input.N, 1, ((1.0 - self.probalility_table[i][j]) * 1e4) as i64);
//                 mcf.add_edge(i, j + input.N, 1, (-self.probalility_table[i][j] * 1e4) as i64);
//             }
//         }

//         // 最小費用流を流す
//         let cost = mcf.min_cost_flow(input.N * 2, input.N * 2 + 1, input.N as isize);

//         // 割当を復元
//         for i in 0..input.N {
//             for &e in mcf.graph[i].iter() {
//                 if e.cap == 0 {
//                     // フローが流れて容量0になった部分が割り当てられた出口セル(self.N ~ self.N * 2の番号になっていることに注意)
//                     self.correspondence[i] = e.to - input.N;
//                 }
//             }
//         }
//     }
//     // 回答の出力
//     fn print(&self) {
//         println!("-1 -1 -1");
//         for &i in self.correspondence.iter() {
//             println!("{}", i);
//         }
//     }
// }

#[derive(Debug, Clone, Copy)]
struct Coordinate {
    y: usize,
    x: usize,
}
impl Coordinate {
    fn new(y: usize, x: usize) -> Self {
        Self { y, x }
    }
    // マンハッタン距離
    fn manhattan_dist(&self, other: &Self) -> usize {
        self.y.abs_diff(other.y) + self.x.abs_diff(other.x)
    }
}

#[derive(Debug, Clone)]
struct Oil {
    n: usize,
    pos_list: Vec<Coordinate>,
    relative_pos_list: Vec<(i64,i64)>,
}

impl Oil {
    fn calc_relative_pos(&mut self) {
        let base_y = self.pos_list[0].y;
        let base_x = self.pos_list[0].x;

        self.relative_pos_list = self
            .pos_list
            .iter()
            .map(|pos| (i64,i64) {
                y: pos[0] - base_y,
                x: pos[1] - base_x,
            })
            .collect();
    }
}

fn main() {
    //開始時刻測定
    get_time();

    // 入力
    // 入力用のBufReaderを作成
    let stdin = io::stdin();
    let mut reader = stdin.lock();

    // インタラクティブ入力処理
    let mut input_line = String::new();
    reader.read_line(&mut input_line).unwrap();
    let mut iter = input_line.trim().split_whitespace();
    let n: usize = iter.next().unwrap().parse().unwrap();
    let m: usize = iter.next().unwrap().parse().unwrap();
    let eps: f64 = iter.next().unwrap().parse().unwrap();

    let mut oils_vec = Vec::new();
    for _ in 0..m {
        let mut input_line = String::new();
        reader.read_line(&mut input_line).unwrap();
        let mut iter = input_line.trim().split_whitespace();
        let oil_n: usize = iter.next().unwrap().parse().unwrap();
        let yx: Vec<Coordinate> = (0..n)
            .map(|_| Coordinate {
                y: iter.next().unwrap().parse().unwrap(),
                x: iter.next().unwrap().parse().unwrap(),
            })
            .collect();

        let mut pos_list = Vec::new();
        for coord in yx {
            pos_list.push(coord);
        }

        let mut oil = Oil {
            n: oil_n,
            pos_list,
            relative_pos_list: Vec::new(), // Initialize relative_pos_list
            // Initialize other fields as needed
        };

        oil.calc_relative_pos(); // Calculate relative_pos_list
        oils_vec.push(oil);
    }

    // デバッグ
    for oil in &oils_vec {
        println!("#c {:?}", oil);
    }

    // let mut state = State::new(&input);
    // state.init_power(&input);

    // state.solve(&mut source, &input);
    
    // state.detect_correspondence(&input);
    // state.print();

    eprintln!("time: {}ms", get_time());
}