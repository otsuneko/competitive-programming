#![allow(dead_code,unused_imports,unused_variables,non_snake_case, non_upper_case_globals, path_statements)]
use bitvec::vec;
use proconio::{fastout, input,marker::{Chars, Bytes, Isize1, Usize1}};
use std::{
    cmp::{max, min, Reverse},
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    mem::swap,
    process::exit,
};
use itertools::Itertools;
use superslice::Ext;
use rustc_hash::FxHashMap;
use rand::prelude::*;
use rand::Rng;

const INF: usize = usize::MAX;
const TIME_LIMIT: f64 = 3.0;

#[derive(Debug,Clone)]
pub struct Rect {
    x1: usize, // 左上のx座標
    y1: usize, // 左上のy座標
    x2: usize, // 右下のx座標
    y2: usize, // 右下のy座標
    area: usize, // 面積
    col_id: usize, // どの列に配置するか
    req_id: usize // どの顧客希望面積に対応するか(暫定。処理途中で値バグるかも)
}

pub struct Solve {
    W: usize, // 幅と高さ。1000固定
    D: usize, // 日数。5~50の一様分布
    N: usize, // 日毎の長方形数。5~50の一様分布
    req_areas: Vec<Vec<usize>>, // 日毎の顧客希望面積一覧(昇順)
}

impl Solve {
    pub fn new(w: usize, d:usize, n:usize, req_areas:Vec<Vec<usize>>) -> Self {
        Self {
            W: w,
            D: d,
            N: n,
            req_areas: req_areas,
        }
    }

    pub fn solve(&self) {

        // 時間計測
        get_time();

        // 乱数生成器
        let mut rng = rand_pcg::Pcg64Mcg::seed_from_u64(890482);

        // ステップ１：列の分割数を変えながら探索面積が大きいものから貪欲に配置
        // 先頭行から順番に必要な面積をカバーできるだけの行を選択していく
        // 配置した長方形は各列の高さの差が最小となるよう列ごとに管理
        let mut best_cost = INF;
        let min_cols_num:usize = if self.N < 30 { 1 } else { 3 }; // 列を最小何分割するか
        let max_cols_num:usize = if self.N < 30 { 6 } else { 10 }; // 列を最大何分割するか
        let mut best_rects:Vec<Vec<Rect>> = vec![vec![];self.D]; // 日毎の長方形配置
        let mut best_col_rects:Vec<Vec<Vec<Rect>>> = vec![vec![vec![];max_cols_num];self.D]; // 日毎と列毎の長方形配置
        for total_cols_num in min_cols_num..=max_cols_num {
            // D日分の処理
            let mut rects:Vec<Vec<Rect>> = vec![vec![];self.D];
            let mut col_rects:Vec<Vec<Vec<Rect>>> = vec![vec![vec![];total_cols_num];self.D];
            for d in 0..self.D {
                let col_len = self.W / total_cols_num;
                let mut rows = vec![0;total_cols_num];
                // N個の長方形を大きい順に配置
                for n in (0..self.N).rev() {
                    // 全列の縦の長さの残差平方和が最小になる列を選択
                    let mut squared_sum = vec![INF;total_cols_num];
                    let mut add_rows = vec![0;total_cols_num];
                    for col in 0..total_cols_num {
                        // 既に長方形で埋まっている列はスキップ
                        if rows[col] == self.W {
                            continue;
                        }
                        // 仮に追加した場合の残差平方和を計算
                        let mut tmp_rows = rows.clone();
                        for add_row in 1..=self.W {
                            if add_row * col_len >= self.req_areas[d][n] || rows[col] + add_row == self.W {
                                tmp_rows[col] += add_row;
                                add_rows[col] = add_row;
                                break;
                            }
                        }

                        let rect_area = add_rows[col] * col_len;

                        // 残差平方和の計算時、充填率0の列は1個にまとめる
                        let cnt_zero = tmp_rows.iter().filter(|&r| *r == 0).count();
                        let mean = tmp_rows.iter().sum::<usize>() / (total_cols_num - cnt_zero);
                        let mut sum = 0;
                        for r in tmp_rows.iter() {
                            sum += (r - mean).pow(2);
                        }
                        squared_sum[col] = sum;
                        // 希望面積との差分が大きい場合はペナルティ
                        if self.req_areas[d][n] > rect_area {
                            squared_sum[col] *= self.req_areas[d][n] - rect_area;
                        }
                    }

                    // 最小の残差平方和を持つ列のインデックスを取得
                    // TODO: 希望面積との差分の少なさも評価値に加える
                    let mut min_col = 0;
                    let mut min_val = INF;
                    for col in 0..total_cols_num {
                        if squared_sum[col] < min_val {
                            min_val = squared_sum[col];
                            min_col = col;
                        }
                    }

                    // 長方形を追加
                    let rect = Rect{
                        x1: min_col*col_len,
                        y1: rows[min_col],
                        x2: (min_col+1)*col_len,
                        y2: rows[min_col]+add_rows[min_col],
                        area: add_rows[min_col] * col_len,
                        col_id: min_col,
                        req_id: n
                    };
                    rects[d].push(rect.clone());
                    col_rects[d][min_col].push(rect.clone());
                    rows[min_col] += add_rows[min_col];
                }
            }
            // スコアが最大の場合を採用
            let cost = self.compute_cost(&mut rects);
            if cost < best_cost {
                best_cost = cost;
                best_rects = rects.clone();
                best_col_rects = col_rects.clone();
            }
        }

        // ステップ２：パーティションのズレ補正その１
        // 左側の列に面積の大きい長方形を配置し、右側の列に面積の小さい長方形を配置する
        let total_cols_num = best_col_rects[0].len(); // 全体の列数
        let col_len = self.W / total_cols_num;
        let mut weighted_col_rects = vec![vec![vec![];total_cols_num];self.D]; // 日毎と列毎の長方形配置
        let mut rects = best_rects.clone();

        // 左の列から順に面積50%を超えるまでなるべく面積の大きい長方形を空白が出ないように埋めていく
        let left_cols_num = (weighted_col_rects[0].len() + 1) / 2; // 大きい長方形を敷き詰める左側の列数

        // 左側col_num列に割り振る長方形を決定する
        // D日分繰り返す
        for d in 0..self.D {
            let mut height_list = best_rects[d].iter().map(|r| r.y2 - r.y1).collect::<Vec<usize>>();
            height_list.sort_by(|a, b| b.cmp(a)); // 高さの降順にソート
            let mut best_score = 0.0;
            let mut best_col_rect_ids = vec![vec![];left_cols_num];// その列に割り振られた長方形のid
            let mut best_col_heights = vec![0;total_cols_num]; // その列の合計の高さ
            let mut best_used_rects = vec![]; // 使われた長方形のid


            let mut col_rect_ids = vec![vec![];left_cols_num]; // その列に割り振られた長方形のid
            let mut col_heights = vec![0;total_cols_num]; // その列の合計の高さ
            // 左の列から埋められる限り大きい長方形を埋める
            let mut used_rects = vec![false;self.N];
                for n in 0..self.N {
                    for col in 0..left_cols_num {
                        if col_heights[col] + height_list[n] <= self.W && !used_rects[n]{
                            col_rect_ids[col].push(n);
                            col_heights[col] += height_list[n];
                            used_rects[n] = true;
                        }
                    }
                }

            // スコア計算
            let score = self.compute_fill_score(d, &height_list, &col_rect_ids, &col_heights);

            // スコアが改善されたら更新
            if score > best_score {
                best_score = score;
                best_col_rect_ids = col_rect_ids.clone();
                best_col_heights = col_heights.clone();
                best_used_rects = used_rects.clone();
            }

            if best_score == 0.0 {
                continue;
            }

            // 左側の列に割り振られた長方形を配置する
            rects[d].sort_by_key(|r| r.y1 - r.y2); // 高さの降順にソート
            for col in 0..left_cols_num {
                let mut cur_height = 0;
                for &n in &best_col_rect_ids[col] {
                    let mut rect = rects[d][n].clone();
                    let rect_height = rect.y2 - rect.y1;
                    rect.x1 = col * col_len;
                    rect.y1 = cur_height;
                    rect.x2 = (col + 1) * col_len;
                    rect.y2 = cur_height + rect_height;
                    rect.col_id = col;
                    weighted_col_rects[d][col].push(rect);
                    cur_height += rect_height;
                }
            }

            // 残りの列は高さの残差平方和が最小になるように長方形を配置
            let unused_rect_ids = (0..self.N).filter(|&n| !best_used_rects[n]).collect::<Vec<usize>>();
            let mut col_heights = best_col_heights.clone();
            let mut is_ok = true;
            for n in unused_rect_ids {
                let mut squared_sum = vec![INF;total_cols_num];
                let rect_height = rects[d][n].y2 - rects[d][n].y1;
                for col in left_cols_num..total_cols_num {
                    // 仮に追加した場合の残差平方和を計算
                    let mut tmp_col_height = col_heights.clone();
                    if col_heights[col] + rect_height <= self.W {
                        tmp_col_height[col] += rect_height;
                    }

                    // 残差平方和の計算時、充填率0の列は1個にまとめる
                    let cnt_zero = tmp_col_height.iter().filter(|&r| *r == 0).count();
                    if (total_cols_num - left_cols_num) - cnt_zero == 0 {
                        continue;
                    }
                    let mean = tmp_col_height.iter().sum::<usize>() / ((total_cols_num - left_cols_num) - cnt_zero);
                    let mut sum = 0;
                    for r in tmp_col_height.iter() {
                        sum += (r - mean).pow(2);
                    }
                    squared_sum[col] = sum;
                }

                // 最小の残差平方和を持つ列のインデックスを取得
                let mut min_col = left_cols_num;
                let mut min_val = INF;
                for col in left_cols_num..total_cols_num {
                    if squared_sum[col] < min_val {
                        min_val = squared_sum[col];
                        min_col = col;
                    }
                }

                // 長方形を更新して配置
                rects[d][n].x1 = min_col*col_len;
                rects[d][n].y1 = col_heights[min_col];
                rects[d][n].x2 = (min_col+1)*col_len;
                rects[d][n].y2 = col_heights[min_col] + rect_height;
                rects[d][n].col_id = min_col;
                if rects[d][n].y1 > self.W || rects[d][n].y2 > self.W {
                    is_ok = false;
                    break;
                }
                weighted_col_rects[d][min_col].push(rects[d][n].clone());
                col_heights[min_col] += rect_height;
            }

            // 長方形配置の妥当性確認
            let mut num_rects = 0;
            for col in 0..total_cols_num {
                num_rects += weighted_col_rects[d][col].len();
                for n in 0..weighted_col_rects[d][col].len() {
                    let rect = &weighted_col_rects[d][col][n];
                    if rect.x1 >= rect.x2 || rect.y1 >= rect.y2 {
                        is_ok = false;
                        break;
                    }
                }
                if col_heights[col] > self.W {
                    is_ok = false;
                    break
                }
            }
            if num_rects != self.N {
                is_ok = false;
            }
            if is_ok {
                best_col_rects[d] = weighted_col_rects[d].clone();
            }
        }

        // ステップ３：希望面積に満たない長方形の幅拡張による面積調整
        self.extend_height(&mut best_col_rects);
        self.extend_col_len(&mut best_col_rects);

        // ステップ３：パーティションのズレ補正その２
        // 山登りで時間いっぱい前日のパーティション位置に揃えられるだけ揃える
        // let mut cnt = 0;
        // loop {
        //     cnt += 1;
        //     if cnt%100 == 0 {
        //         let t = get_time() / TIME_LIMIT as f64;
        //         if t >= 1.0 {
        //             break;
        //         }
        //     }

        //     // 乱数で日付と列を選択
        //     let d = rng.gen_range(1..self.D-1);
        //     let col = rng.gen_range(0..total_cols_num);

        //     // その列の長方形が0個の場合はスキップ
        //     if best_col_rects[d][col].len() == 0 || best_col_rects[d-1][col].len() == 0 || best_col_rects[d+1][col].len() == 0{
        //         continue;
        //     }

        //     // d-1日～d+1日までのcol列目の長方形の高さの累積和を計算
        //     let mut col_heights_prev = vec![0;best_col_rects[d-1][col].len()];
        //     let mut col_heights_now = vec![0;best_col_rects[d][col].len()];
        //     let mut col_heights_next = vec![0;best_col_rects[d+1][col].len()];
        //     for diff in -1..2 {
        //         let d = d as i32 + diff;
        //         for n in 0..best_col_rects[d as usize][col].len() {
        //             if diff == -1 {
        //                 col_heights_prev[n] = best_col_rects[d as usize][col][n].y2;
        //             } else if diff == 0 {
        //                 col_heights_now[n] = best_col_rects[d as usize][col][n].y2;
        //             } else {
        //                 col_heights_next[n] = best_col_rects[d as usize][col][n].y2;
        //             }
        //         }
        //     }
        //     // d-1日目とd日目か、d日目とd+1日目で高さの差分が最小となる箇所を見つける
        //     let mut min_diff = INF;
        //     let mut start_d = INF;
        //     let mut prev_n = INF;
        //     let mut next_n = INF;
        //     for prev_y in col_heights_prev.iter() {
        //         for now_y in col_heights_now.iter() {
        //             let diff = (*prev_y as i32 - *now_y as i32).abs() as usize;
        //             if diff != 0 && diff < min_diff {
        //                 min_diff = diff;
        //                 start_d = d-1;
        //                 prev_n = col_heights_prev.iter().position(|&r| r == *prev_y).unwrap_or(INF);
        //                 next_n = col_heights_now.iter().position(|&r| r == *now_y).unwrap_or(INF);
        //             }
        //         }
        //     }
        //     for now_y in col_heights_now.iter() {
        //         for next_y in col_heights_next.iter() {
        //             let diff = (*now_y as i32 - *next_y as i32).abs() as usize;
        //             if diff < min_diff {
        //                 min_diff = diff;
        //                 start_d = d;
        //                 prev_n = col_heights_now.iter().position(|&r| r == *now_y).unwrap_or(INF);
        //                 next_n = col_heights_next.iter().position(|&r| r == *next_y).unwrap_or(INF);
        //             }
        //         }
        //     }

        //     // 高さの差分が最小となる箇所に合わせて長方形を移動
        //     if min_diff == INF || start_d == INF || prev_n == INF || next_n == INF {
        //         continue
        //     }

        //     // 変更前のコストを計算
        //     let prev_cost = self.compute_cost_col(&best_col_rects[start_d][col], &best_col_rects[start_d+1][col]);

        //     let prev_y = best_col_rects[start_d][col][prev_n].y2;
        //     let next_y = best_col_rects[start_d+1][col][next_n].y2;
        //     // 低い方の高さを高い方に合わせる
        //     let target_d;
        //     let max_height;
        //     let start_n;
        //     if prev_y > next_y {
        //         target_d = start_d+1;
        //         max_height = next_y;
        //         start_n = next_n;
        //     } else {
        //         target_d = start_d;
        //         max_height = prev_y;
        //         start_n = prev_n;
        //     }

        //     // 高さをあわせた結果、長方形が上限高さを超える場合はスキップ
        //     if max_height + min_diff > self.W {
        //         continue;
        //     }

        //     // 低い方の長方形を高い方の長方形に合わせる
        //     let before_rects = best_col_rects[target_d][col].clone();
        //     for n in start_n..best_col_rects[target_d][col].len() {
        //         // 最初の長方形は、y2を高い方の長方形の高さに合わせる
        //         if n == start_n {
        //             best_col_rects[target_d][col][n].y2 += min_diff;
        //         } else {
        //             best_col_rects[target_d][col][n].y1 = best_col_rects[target_d][col][n-1].y2;
        //             if best_col_rects[target_d][col][n].y2 + min_diff < self.W {
        //                 best_col_rects[target_d][col][n].y2 += min_diff;
        //             } else {
        //                 best_col_rects[target_d][col][n].y2 = self.W;
        //             }
        //         }
        //     }

        //     // 変更後のコストを計算
        //     let next_cost = self.compute_cost_col(&best_col_rects[start_d][col], &best_col_rects[start_d+1][col]);

        //     // 全体スコアが減るなら採用
        //     dbg!(prev_cost, next_cost);
        //     if next_cost < prev_cost {
        //         continue;
        //     }

        //     // スコアが改善されない場合は元に戻す
        //     best_col_rects[target_d][col] = before_rects;
        // }

        // 各列の面積の小さい長方形から順に、D日間全てで高さをあわせて一番下に移動していく
        let mut cur_height = vec![vec![self.W;total_cols_num];self.D];
        let mut stop_flg = vec![vec![false;total_cols_num];self.D];
        for col in 0..total_cols_num {
            let mut cnt = 0;
            while cnt < self.N {
                // 一番下の長方形のD日間の最大高さを取得
                let mut max_height = 0;
                for d in 0..self.D {
                    if stop_flg[d][col] || best_col_rects[d][col].len() == 0 {
                        continue;
                    }
                    if best_col_rects[d][col].len() < cnt+1 {
                        stop_flg[d][col] = true;
                        continue
                    }
                    let n = best_col_rects[d][col].len() - 1 - cnt;
                    let height = best_col_rects[d][col][n].y2 - best_col_rects[d][col][n].y1;
                    max_height = max(max_height, height);
                }

                // まだ底に移動していない一番下の長方形を底に移動し、最大高さに合わせる
                for d in 0..self.D {
                    if stop_flg[d][col] || best_col_rects[d][col].len() == 0  {
                        continue;
                    }
                    if best_col_rects[d][col].len() < cnt+1 {
                        stop_flg[d][col] = true;
                        continue
                    }
                    let n = best_col_rects[d][col].len() - 1 - cnt;
                    if (n > 0 && cur_height[d][col] < best_col_rects[d][col][n-1].y2 + max_height) || (n == 0 && cur_height[d][col] < max_height) {
                        stop_flg[d][col] = true;
                        continue;
                    }
                    best_col_rects[d][col][n].y1 = cur_height[d][col] - max_height;
                    best_col_rects[d][col][n].y2 = cur_height[d][col];
                    best_col_rects[d][col][n].area = max_height * col_len;
                    cur_height[d][col] -= max_height;
                }
                cnt += 1;
            }
        }

        // ステップ４：希望面積に満たない長方形の面積補正

        // 各列の長方形が縦に隙間なく配置されるように高さを調整
        self.adjust_height(&mut best_col_rects);

        // best_col_rectsから日毎に面積で昇順ソートされたbest_rectsを復元
        let mut best_rects = vec![vec![];self.D];
        for d in 0..self.D {
            for col in 0..best_col_rects[d].len() {
                for n in 0..best_col_rects[d][col].len() {
                    let rect = best_col_rects[d][col][n].clone();
                    best_rects[d].push(rect);
                }
            }
            best_rects[d].sort_by_key(|r| r.area);
        }

        // 回答出力
        for d in 0..self.D {
            for n in 0..self.N {
                println!("{} {} {} {}", best_rects[d][n].y1, best_rects[d][n].x1, best_rects[d][n].y2, best_rects[d][n].x2);
            }
        }
    }

    // 作成した長方形が他の長方形と重ならないかチェック
    fn is_overlap(&self, x1:usize, y1:usize, x2:usize, y2:usize, rects:&Vec<Rect>, n:usize) -> bool {
        for i in 0..rects.len() {
            if i == n {
                continue;
            }
            let (x3,y3,x4,y4) = (rects[i].x1,rects[i].y1,rects[i].x2,rects[i].y2);
            if max(x1, x3) < min(x2, x4) && max(y1, y3) < min(y2, y4) {
                return true;
            }
        }
        return false;
    }

    // スコア計算(なるべく少ない数の長方形を空白が出ないよう並べられるほど高スコア)
    fn compute_fill_score(&self, d:usize, height_list:&Vec<usize>, col_rect_ids:&Vec<Vec<usize>>, col_heights:&Vec<usize>) -> f64 {
        let total_cols_num = col_heights.len(); // 全体の列数
        let left_cols_num = col_rect_ids.len(); // 処理対象の列数
        let mut fill_rate = 0.0; // 対象列の充填率
        let mut num_used_rects = 0; // 対象列で使われている長方形の数
        let unused_rects_area; // 使わなかった長方形の合計面積
        for col in 0..left_cols_num {
            fill_rate += col_heights[col] as f64;
            num_used_rects += col_rect_ids[col].len();
        }
        unused_rects_area = height_list.iter().sum::<usize>() - fill_rate as usize;
        fill_rate /= self.W as f64 * col_rect_ids.len() as f64;

        let score;
        // 使われていない長方形の面積の合計が残りの全面積を超えた場合はペナルティ
        if unused_rects_area - (total_cols_num - left_cols_num) * self.W > 0 {
            score = 1e20 * fill_rate.powf(0.5) / num_used_rects as f64 / (unused_rects_area - (total_cols_num - left_cols_num) * self.W) as f64;
        } else {
            score = 0.0;
        }
        score
    }

    // 各列の一番下にいる長方形が希望面積を満たさずまだ下に伸ばせる場合、面積を満たすまで伸ばす
    fn extend_height(&self, col_rects:&mut Vec<Vec<Vec<Rect>>>) {
        for d in 0..self.D {
            for col in 0..col_rects[d].len() {
                if col_rects[d][col].len() == 0 {
                    continue;
                }
                let n = col_rects[d][col].len() - 1;
                let req_area = self.req_areas[d][col_rects[d][col][n].req_id];
                let mut cur_area = col_rects[d][col][n].area;
                if cur_area >= req_area {
                    continue;
                }
                loop {
                    let (width, height) = (col_rects[d][col][n].x2 - col_rects[d][col][n].x1, col_rects[d][col][n].y2 - col_rects[d][col][n].y1);
                    cur_area = width * height;
                    if cur_area >= req_area || col_rects[d][col][n].y2 == self.W {
                        break;
                    }
                    col_rects[d][col][n].y2 += 1;
                    col_rects[d][col][n].area = width * (height + 1);
                }
            }
        }
    }

    // 希望面積に満たない長方形を含む列の横幅を拡張し、別の列の横幅を狭める
    fn extend_col_len(&self, col_rects:&mut Vec<Vec<Vec<Rect>>>) {
        // 1列しかない場合は処理しない
        if col_rects[0].len() == 1 {
            return;
        }

        for d in 0..self.D {
            // 日毎に最も希望面積を満たしていない長方形を発見
            let mut max_lack_area = 0;
            let mut max_lack_rect = (INF,INF); // (列id, 長方形id)
            for col in 0..col_rects[d].len() {
                for n in 0..col_rects[d][col].len() {
                    let rect = &col_rects[d][col][n];
                    if rect.area < self.req_areas[d][rect.req_id] && rect.area > max_lack_area {
                        max_lack_area = rect.area;
                        max_lack_rect = (col,n);
                    }
                }
            }

            // 試しに0列目の長方形が高さself.Wかつ希望面積を満たさない場合だけを解消
            let (col,n) = max_lack_rect;
            if (col,n) == (INF,INF) || col_rects[d][col][n].y2 - col_rects[d][col][n].y1 != self.W {
                continue;
            }

            // 0列目の幅をどれだけ広げれば希望面積を満たすか計算
            let lack_col_len = ((self.req_areas[d][col_rects[d][col][n].req_id] - col_rects[d][col][n].area) + self.W - 1) / self.W;

            // 各列の長方形の合計高さを管理
            let mut col_total_heights = vec![0;col_rects[d].len()];
            for col in 0..col_rects[d].len() {
                for n in 0..col_rects[d][col].len() {
                    col_total_heights[col] += col_rects[d][col][n].y2 - col_rects[d][col][n].y1;
                }
            }

            // 右端から順に他の列の長方形の横幅を狭める
            let mut total_extend_col_len = 0;
            for col in (1..col_rects[d].len()).rev() {
                // 希望面積の不足分が0なら終了
                if total_extend_col_len >= lack_col_len {
                    break;
                }

                // 伸ばせる限り縦に伸ばす
                loop {
                    // 希望面積の不足分が0なら終了
                    if total_extend_col_len >= lack_col_len {
                        break;
                    }

                    // 希望面積を満たすように幅を縮めて高さを伸ばした時に合計高さがself.Wを超えたら終了
                    let mut add_rows = vec![0;col_rects[d][col].len()];
                    for n in 0..col_rects[d][col].len() {
                        // 幅を1縮めた時に各長方形の高さをどれだけ伸ばせばいいか計算
                        let (width, height) = (col_rects[d][col][n].x2 - col_rects[d][col][n].x1, col_rects[d][col][n].y2 - col_rects[d][col][n].y1);
                        let new_area = (width - 1) * height;
                        let req_area = self.req_areas[d][col_rects[d][col][n].req_id];
                        if new_area >= req_area {
                            continue;
                        }
                        let lack_area = req_area - new_area;
                        for row in 1..=self.W {
                            if (width - 1) * row >= lack_area {
                                add_rows[n] = row;
                                break;
                            }
                        }
                    }
                    // 各長方形の高さを追加した時に合計高さがself.Wを超えたら終了
                    let su = add_rows.iter().sum::<usize>();
                    if col_total_heights[col] + su > self.W {
                        break;
                    }
                    col_total_heights[col] += su;

                    // 各長方形の幅と高さと面積を更新
                    let mut total_add_height = 0;
                    for n in 0..col_rects[d][col].len() {
                        col_rects[d][col][n].x1 += 1;
                        if n > 0 {
                            col_rects[d][col][n].y1 = col_rects[d][col][n-1].y2;
                        }
                        total_add_height += add_rows[n];
                        col_rects[d][col][n].y2 += total_add_height;
                        col_rects[d][col][n].area = (col_rects[d][col][n].x2 - col_rects[d][col][n].x1) * (col_rects[d][col][n].y2 - col_rects[d][col][n].y1);
                    }
                    total_extend_col_len += 1;
                }
            }

            // 右端の列から列間の隙間を埋めていく
            for col in (0..col_rects[d].len()-1).rev() {
                for n in 0..col_rects[d][col].len() {
                    // 0列目以外は列を右側にシフトさせていく
                    let shift_len = col_rects[d][col+1][0].x1 - col_rects[d][col][n].x2;
                    if col > 0 {
                        col_rects[d][col][n].x1 += shift_len;
                        col_rects[d][col][n].x2 += shift_len;
                    } else {
                        // 0列目は右端を伸ばすだけ
                        col_rects[d][col][n].x2 += shift_len;
                    }
                }
            }
        }
    }

    fn adjust_height(&self, col_rects: &mut Vec<Vec<Vec<Rect>>>) {
        let total_cols_num = col_rects[0].len();
        let mut cur_height = vec![vec![0;total_cols_num];self.D];
        for d in 0..self.D {
            for col in 0..total_cols_num {
                if col_rects[d][col].len() == 0 {
                    continue;
                }
                let col_rects_num = col_rects[d][col].len();
                let col_len = col_rects[d][col][0].x2 - col_rects[d][col][0].x1;
                col_rects[d][col][0].y1 = 0;
                for n in 0..col_rects_num-1 {
                    if col_rects[d][col][n].y2 == col_rects[d][col][n+1].y1 {
                        let height = col_rects[d][col][n].y2 - col_rects[d][col][n].y1;
                        cur_height[d][col] += height;
                        continue;
                    }
                    let new_height = col_rects[d][col][n+1].y1 - col_rects[d][col][n].y1;
                    col_rects[d][col][n].y1 = cur_height[d][col];
                    col_rects[d][col][n].y2 = cur_height[d][col] + new_height;
                    col_rects[d][col][n].area = new_height * col_len;
                    cur_height[d][col] += new_height;
                }
                col_rects[d][col][col_rects_num-1].y2 = self.W;
            }
        }
    }

    fn compute_cost_col(&self, rects_before: &Vec<Rect>, rects_after: &Vec<Rect>) -> usize {
        let mut cost = 0;
        let mut hs = BTreeSet::new();
        let mut vs = BTreeSet::new();
        let mut hs2 = BTreeSet::new();
        let mut vs2 = BTreeSet::new();

        // 前日のパーティション位置
        for n in 0..rects_before.len() {
            let (y1, x1, y2, x2) = (rects_before[n].y1, rects_before[n].x1, rects_before[n].y2, rects_before[n].x2);
            for x in x1..x2 {
                if y1 > 0 {
                    hs.insert((y1, x));
                }
                if y2 < self.W {
                    hs.insert((y2, x));
                }
            }
            for y in y1..y2 {
                if x1 > 0 {
                    vs.insert((x1, y));
                }
                if x2 < self.W {
                    vs.insert((x2, y));
                }
            }
        }
        // 当日のパーティション位置
        for n in 0..rects_after.len() {
            let (y1, x1, y2, x2) = (rects_after[n].y1, rects_after[n].x1, rects_after[n].y2, rects_after[n].x2);
            for x in x1..x2 {
                if y1 > 0 {
                    hs2.insert((y1, x));
                }
                if y2 < self.W {
                    hs2.insert((y2, x));
                }
            }
            for y in y1..y2 {
                if x1 > 0 {
                    vs2.insert((x1, y));
                }
                if x2 < self.W {
                    vs2.insert((x2, y));
                }
            }
        }

        for &(y, x) in &hs {
            if !hs2.contains(&(y, x)) {
                cost += 1;
            }
        }
        for &(x, y) in &vs {
            if !vs2.contains(&(x, y)) {
                cost += 1;
            }
        }
        for &(y, x) in &hs2 {
            if !hs.contains(&(y, x)) {
                cost += 1;
            }
        }
        for &(x, y) in &vs2 {
            if !vs.contains(&(x, y)) {
                cost += 1;
            }
        }
        (cost+1) as usize
    }


    // スコア計算(希望面積との差、前日のパーティションとのずれを考慮)
    // スコアは小さいほど良いことに注意
    fn compute_cost(&self, rects: &mut Vec<Vec<Rect>>) -> usize {

        let mut cost = 0;
        let mut hs = BTreeSet::new();
        let mut vs = BTreeSet::new();
        for d in 0..self.D {
            // 長方形同士が重なっていないかチェックし、重なっている場合は最大スコアを返す
            for p in 0..self.N {
                // 長方形の面積が0になっていないかチェックし、0になっている場合は最大スコアを返す
                if rects[d][p].area == 0 || rects[d][p].x1 >= rects[d][p].x2 || rects[d][p].y1 >= rects[d][p].y2{
                    return INF;
                }
                for q in 0..p {
                    if max(rects[d][p].x1, rects[d][q].x1) < min(rects[d][p].x2, rects[d][q].x2) &&
                       max(rects[d][p].y1, rects[d][q].y1) < min(rects[d][p].y2, rects[d][q].y2)
                    {
                        return INF;
                    }
                }
            }
            rects[d].sort_by_key(|r| r.area);
            let mut hs2 = BTreeSet::new();
            let mut vs2 = BTreeSet::new();

            // 希望面積との差
            for n in 0..self.N {
                let (y1, x1, y2, x2) = (rects[d][n].y1, rects[d][n].x1, rects[d][n].y2, rects[d][n].x2);
                let b = (y2 - y1) * (x2 - x1);
                if self.req_areas[d][n] > b {
                    cost += 100 * (self.req_areas[d][n] - b) as i64;
                }
                for x in x1..x2 {
                    if y1 > 0 {
                        hs2.insert((y1, x));
                    }
                    if y2 < self.W {
                        hs2.insert((y2, x));
                    }
                }
                for y in y1..y2 {
                    if x1 > 0 {
                        vs2.insert((x1, y));
                    }
                    if x2 < self.W {
                        vs2.insert((x2, y));
                    }
                }
            }
            // 前日のパーティションとのずれ
            if d > 0 {
                for &(y, x) in &hs {
                    if !hs2.contains(&(y, x)) {
                        cost += 1;
                    }
                }
                for &(x, y) in &vs {
                    if !vs2.contains(&(x, y)) {
                        cost += 1;
                    }
                }
                for &(y, x) in &hs2 {
                    if !hs.contains(&(y, x)) {
                        cost += 1;
                    }
                }
                for &(x, y) in &vs2 {
                    if !vs.contains(&(x, y)) {
                        cost += 1;
                    }
                }
            }
            hs = hs2;
            vs = vs2;
        }
        (cost + 1) as usize
    }
}

#[fastout]
fn main() {
    input! {
        w: usize,
        d: usize,
        n: usize,
        req_areas: [[usize;n];d]
    }

    let solve = Solve::new(w,d,n,req_areas);
    solve.solve();

}

////////////////////////////////////////
// ここから下はテンプレート
////////////////////////////////////////
pub fn get_time() -> f64 {
	static mut STIME: f64 = -1.0;
	let t = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap();
	let ms = t.as_secs() as f64 + t.subsec_nanos() as f64 * 1e-9;
	unsafe {
		if STIME < 0.0 {
			STIME = ms;
		}
		ms - STIME
	}
}
