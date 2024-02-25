#include <iostream>
#include <vector>
#include <cmath>
#include <tuple>
#include <set>
#include <tuple>
#include <algorithm>
#include <cassert>
#include <chrono>
#include <queue>
#include "./cpp-dump/dump.hpp"

#define print(x) cerr << x << endl
#define prints(x,y) cerr << x << " " << y << endl

using namespace std;
using namespace chrono;

const long long INF = 1e18;
const double TIME_LIMIT = 2.8;

const int INI_SWITCH_M = 2; // 初期方針を切り替えるMの閾値
const int FORECAST_INTERVAL = 2; // ポリオミノの形そのままで占う時の間隔
const int RESEARCH_TOP_K = 3; // ポリオミノの形そのままで占った結果、v(S)上位何個に対し隣接マスを再調査するか
const int FORECAST_LEN = 3;// 占う正方形領域の一辺の長さ
const int TRIAL_DIG_SWITCH_TURN = 140; // 試し掘り方式からBFSでの隣接マス発掘方式に切り替えるターン
const int TRIAL_DIG_NUM = 5; // 1ターンで何回試し掘りするか
const int DIST_THRESHOLD = 4; // 試し掘りをしていく時に直前に掘った座標と離すべきマンハッタン距離の閾値
const int DIST_WEIGHT = 1.5; // 試し掘りの候補マスの隣接マスにv(y,x)>0のマスがある場合の重み
const int DFS_LIMIT = 1e6; // DFSで全探索する上限の組合せ数

double get_time(high_resolution_clock::time_point &begin) {
  high_resolution_clock::time_point end = high_resolution_clock::now();
  return chrono::duration<double>(end - begin).count();
}

struct Coordinate;
struct Coordinate {
    int y, x;

    // 追加: デフォルトコンストラクタ
    Coordinate() : y(0), x(0) {}

    // 追加: コンストラクタ
    Coordinate(int y, int x) : y(y), x(x) {}

    // 比較演算子 == のオーバーロード
    bool operator==(const Coordinate& other) const {
        return tie(y, x) == tie(other.y, other.x);
    }

    // 比較演算子 < のオーバーロード
    bool operator<(const Coordinate& other) const {
        return tie(y, x) > tie(other.y, other.x);
    }
};
using FloatCoordinatePair = tuple<float, Coordinate>;
using FloatCoordinateVecPair = tuple<float, vector<Coordinate>>;
const vector<Coordinate> MOVE = {Coordinate(1, 0), Coordinate(-1, 0), Coordinate(0, 1), Coordinate(0, -1)};
const vector<Coordinate> MOVE_AROUND = {
    Coordinate(-1, -1), Coordinate(-1, 0), Coordinate(-1, 1), 
    Coordinate(0, -1), Coordinate(0, 1), Coordinate(1, -1), 
    Coordinate(1, 0), Coordinate(1, 1)
};

// Pythonのheapqでのソートと微妙に処理が違いそう
// struct Compare {
//     bool operator()(const FloatCoordinatePair& a, const FloatCoordinatePair& b) {
//         return get<0>(a) > get<0>(b);  // 逆順にすることで最小値がトップにくる
//     }
// };

// struct VectorComparator {
//     bool operator()(const std::vector<Coordinate>& a, const std::vector<Coordinate>& b) const {
//         return lexicographical_compare(a.begin(), a.end(), b.begin(), b.end());
//     }
// };

struct OIL {
    int n;
    vector<Coordinate> absolute_pos_list;
    vector<Coordinate> relative_pos_list;

    OIL(int n, const vector<Coordinate>& absolute_pos_list, const vector<Coordinate>& relative_pos_list)
        : n(n), absolute_pos_list(absolute_pos_list), relative_pos_list(relative_pos_list) {}
};

class Judge {
public:
    int N, M;
    float EPS;
    vector<OIL> OILS;

    int turn;
    int turn_limit;
    float cost;
    vector<set<Coordinate>> forecasted_poly_set;
    set<Coordinate> digged_total_pos_set;
    set<Coordinate> digged_oil_pos_set;
    int digged_oil_amount;
    set<Coordinate> definitive_oil_pos_set;
    set<int> definitive_poly_id;
    set<vector<Coordinate>> answered_pos_tuple;

    vector<vector<int>> oil_map;
    vector<vector<float>> oil_forecast_map;
    vector<vector<set<int>>> possible_poly_pos_map;
    vector<vector<set<int>>> definitive_poly_pos_map;

    Judge(int n, int m, float eps, const vector<OIL>& oils):
        N(n), 
        M(m), 
        EPS(eps), 
        OILS(oils), 
        turn(0), 
        turn_limit(2 * n * n), 
        cost(0.0),
        digged_oil_amount(0),
        oil_map(n, vector<int>(n, -1)), 
        oil_forecast_map(n, vector<float>(n, -1.0)),
        possible_poly_pos_map(n, vector<set<int>>(n)),
        forecasted_poly_set(m),
        digged_oil_pos_set(),
        definitive_oil_pos_set(),
        definitive_poly_id(),
        answered_pos_tuple(),
        definitive_poly_pos_map(n, vector<set<int>>(n)) {
            initialize_possible_poly_map();
        }

    int dig_pos(int y, int x) {
        if (turn == turn_limit) {
            return -1;
        }

        vector<int> req = {1, y, x};
        print_vector("q",req);

        turn++;
        cost++;
        int actual_oil_amount = 0;
        cin >> actual_oil_amount;
        // cpp_dump(y,x,actual_oil_amount);

        digged_total_pos_set.insert(Coordinate(y,x));
        if (actual_oil_amount > 0) {
            digged_oil_pos_set.insert(Coordinate(y,x));
            if (oil_map[y][x] != actual_oil_amount) {
                digged_oil_amount += actual_oil_amount;
            }
        }

        oil_map[y][x] = actual_oil_amount;
        update_possible_poly_map();
        return actual_oil_amount;
    }

    void initialize_possible_poly_map() {
        for (int poly_id = 0; poly_id < OILS.size(); ++poly_id) {
            for (int base_y = 0; base_y < N; ++base_y) {
                for (int base_x = 0; base_x < N; ++base_x) {
                    bool failure_flg = false;
                    for (auto& relative_pos : OILS[poly_id].relative_pos_list) {
                        int ny = base_y + relative_pos.y;
                        int nx = base_x + relative_pos.x;
                        if (!(0 <= ny && ny < N && 0 <= nx && nx < N)) {
                            failure_flg = true;
                            break;
                        }
                    }
                    if (!failure_flg) {
                        possible_poly_pos_map[base_y][base_x].insert(poly_id);
                    }
                }
            }
        }
    }

    void update_possible_poly_map() {
        for (int poly_id = 0; poly_id < OILS.size(); ++poly_id) {
            for (int base_y = 0; base_y < N; ++base_y) {
                for (int base_x = 0; base_x < N; ++base_x) {
                    vector<Coordinate> poly_pos;
                    bool failure_flg = false;
                    for (auto& relative_pos : OILS[poly_id].relative_pos_list) {
                        int ny = base_y + relative_pos.y;
                        int nx = base_x + relative_pos.x;
                        if (!(0 <= ny && ny < N && 0 <= nx && nx < N)) {
                            failure_flg = true;
                            break;
                        }
                        if (oil_map[ny][nx] == 0 || (oil_map[ny][nx] > 0 && definitive_poly_pos_map[ny][nx].size() == static_cast<size_t>(oil_map[ny][nx]) && poly_id != *definitive_poly_pos_map[ny][nx].begin())) {
                            failure_flg = true;
                            break;
                        }
                        poly_pos.emplace_back(ny, nx);
                    }
                    if (failure_flg) {
                        possible_poly_pos_map[base_y][base_x].erase(poly_id);
                        continue;
                    }
                }
            }
        }
    }

    float forecast_pos_list(const vector<Coordinate>& pos_list) {
        if (turn == turn_limit) {
            return -1;
        }

        assert(pos_list.size() >= 2);

        vector<int> req = {static_cast<int>(pos_list.size())};
        for (const auto& pos : pos_list) {
            req.push_back(pos.y);
            req.push_back(pos.x);
        }
        print_vector("q",req);

        turn++;
        cost += 1.0 / sqrt(pos_list.size());
        int v_S;
        cin >> v_S;
        float each_v_S = float(v_S) / pos_list.size();

        for (const auto& pos : pos_list) {
            if (oil_forecast_map[pos.y][pos.x] == -1.0) {
                oil_forecast_map[pos.y][pos.x] = each_v_S;
            } else {
                oil_forecast_map[pos.y][pos.x] = (oil_forecast_map[pos.y][pos.x] + each_v_S) / 2;
            }
        }

        return float(v_S);
    }

    int answer(const set<Coordinate>& pos_set) {
        if (turn == turn_limit) {
            return 0;
        }

        // pos_setをソート済みtupleに変換
        // vector<Coordinate> sorted_pos_vector(pos_set.begin(), pos_set.end());
        // comparator

        // tuple<int, int> sorted_pos_tuple;
        // tie(ignore, sorted_pos_tuple) = make_tuple(0, sorted_pos_vector);

        // // Check if the sorted_pos_tuple is in answered_pos_tuple
        // if (answered_pos_tuple.count(sorted_pos_tuple)) {
        //     cerr << "#c same answer in past" << endl;
        //     return;
        // }

        // 回答
        vector<int> req = {static_cast<int>(pos_set.size())};
        for (const auto& pos : pos_set) {
            req.push_back(pos.y);
            req.push_back(pos.x);
        }
        print_vector("a", req);

        turn++;
        int res;
        cin >> res;

        // 回答済みの座標セットに追加
        // answered_pos_tuple.insert(sorted_pos_tuple);
        return res;
    }

    void debug() {
        // cout << "#c " << message << endl;
        cerr << "#c turn = " << turn << endl;
        cerr << "#c cost = " << cost << endl;
        cerr << "#c digged_oil_amount = " << digged_oil_amount << endl;
        cerr << "#c oil_map" << endl;
        for (int y=0;y<N;y++) {
            for (int x=0;x<N;x++) {
                cerr << oil_map[y][x] << " ";
            }
            cerr << endl;
        }
        cerr << "#c oil_forecast_map" << endl;
        for (int y=0;y<N;y++) {
            for (int x=0;x<N;x++) {
                cerr << oil_forecast_map[y][x] << " ";
            }
            cerr << endl;
        }
        cerr << "#c possible_poly_pos_map" << endl;
        for (int y=0;y<N;++y) {
            for (int x=0;x<N;++x) {
                for (const auto& elem: possible_poly_pos_map[y][x]) {
                    cerr << elem << ",";
                }
                if (possible_poly_pos_map[y][x].size() == 0) {
                    cerr << "X,";
                }
                cerr << " ";
            }
            cerr << endl;
        }
        cerr << "#c definitive_poly_pos_map" << endl;
        for (int y=0;y<N;++y) {
            for (int x=0;x<N;++x) {
                for (const auto& elem: definitive_poly_pos_map[y][x]) {
                    cerr << elem << ",";
                }
                if (definitive_poly_pos_map[y][x].size() == 0) {
                    cerr << "X,";
                }
                cerr << " ";
            }
            cerr << endl;
        }
    }

    template <typename T>
    void print_vector(string s, const vector<T>& vec) {
        cout << s << ' ';
        for (const auto& elem : vec) {
            cout << elem << ' ';
        }
        cout << endl;
        cout.flush();
    }
};


class Solver {
    int N;
    int M;
    float EPS;
    vector<OIL> OILS;
    Judge judge;
    high_resolution_clock::time_point start_time;
    double cur_time;

    int cost;
    int score;
    int total_oil_amount;
    vector<FloatCoordinatePair> sorted_v_S_pos_list;

public:
    Solver(int n, int m, float eps, const vector<OIL>& oils):
        N(n), M(m), EPS(eps), OILS(oils), judge(n, m, eps, oils) {
            start_time = high_resolution_clock::now();
            cost = 0;
            score = 0;
            total_oil_amount = calculate_total_oil_amount();
            sorted_v_S_pos_list = {};
        }

    int solve();

private:

    int calculate_total_oil_amount() {
        int total = 0;
        for (const auto& oil : OILS) {
            total += oil.n;
        }
        return total;
    }

    bool judge_if_turn_over(){
        return judge.turn == judge.turn_limit;
    }

    bool judge_if_digged_all(){
        if (judge.digged_oil_amount == total_oil_amount) {
            return true;
        }

        set<Coordinate> check_set(judge.digged_total_pos_set.begin(), judge.digged_total_pos_set.end());
        check_set.insert(judge.definitive_oil_pos_set.begin(), judge.definitive_oil_pos_set.end());
        if (check_set.size() == N*N) {
            return true;
        }
        return false;
    }

    // 島全体に対し、各油田(ポリオミノ)の形状そのままスライドさせて占い、最もv(S)が大きい場所を解とする。
    set<Coordinate> slide_optimal_oil_pos() {
        // 当該油田ポリオミノの全マスが島の範囲内に存在するか判定し座標リストを返す。
        auto calc_forecast_pos_list = [&](int base_y, int base_x, const OIL& oil) -> vector<Coordinate> {
            vector<Coordinate> forecast_pos_list;
            for (const auto& pos : oil.relative_pos_list) {
                int ny = base_y + pos.y;
                int nx = base_x + pos.x;
                if (!(0 <= ny && ny < N && 0 <= nx && nx < N)) {
                    forecast_pos_list.clear();
                    return forecast_pos_list;
                }
                forecast_pos_list.push_back(Coordinate(ny,nx));
            }
            return forecast_pos_list;
        };

        // これまでの占い結果をもとに今回占うポリオミノの領域の推定v(S)が小さそうならスキップする。
        auto judge_if_skip = [&](const vector<Coordinate>& forecast_pos_list) -> bool {
            float estimated_v_S = 0;
            float cnt_not_updated = 0;
            for (const auto& pos : forecast_pos_list) {
                int y = pos.y;
                int x = pos.x;
                if (judge.oil_forecast_map[y][x] == -1.0) {
                    cnt_not_updated++;
                } else {
                    estimated_v_S += judge.oil_forecast_map[y][x];
                }
            }
            if (cnt_not_updated > float(forecast_pos_list.size()) / 2.5) {
                return false;
            }
            return estimated_v_S < 0.2 * float(forecast_pos_list.size());
        };

        // 当該油田ポリオミノの全マスが島の範囲内に存在する場合、占いを実行し最適油田位置を更新する。
        auto forecast_and_update = [&](int i, const OIL& oil, const vector<Coordinate>& forecast_pos_list,
                                       vector<float>& max_v_S, vector<vector<Coordinate>>& best_oil_pos_list) -> float {
            float v_S = -1.0;
            if (forecast_pos_list.size() != oil.n) {
                return v_S;
            }
            v_S = judge.forecast_pos_list(forecast_pos_list);
            if (judge_if_turn_over()) {
                return -1.0;
            }
            if (v_S > max_v_S[i]) {
                max_v_S[i] = v_S;
                best_oil_pos_list[i] = forecast_pos_list;
            }
            return v_S;
        };


        // メイン処理
        vector<float> max_v_S(M, 0.0);
        vector<vector<Coordinate>> best_oil_pos_list(M);
        vector<vector<FloatCoordinatePair>> research_pos_list(M);
        set<Coordinate> oil_pos_set; // 回答用の座標セット格納変数

        // 最初にFORECAST_INTERVALだけ間隔を空けて占い、付近に油田がありそうなマスを再度占うためにv(S)を保存する
        for (int poly_id = 0; poly_id < M; ++poly_id) {
            for (int gr_y = 0; gr_y < N / FORECAST_INTERVAL; ++gr_y) {
                for (int gr_x = 0; gr_x < N / FORECAST_INTERVAL; ++gr_x) {
                    int base_y = gr_y * FORECAST_INTERVAL;
                    int base_x = gr_x * FORECAST_INTERVAL;

                    auto forecast_pos_list = calc_forecast_pos_list(base_y, base_x, OILS[poly_id]);
                    if (forecast_pos_list.size() == 0) {
                        continue;
                    }
                    if (poly_id > 0 && judge_if_skip(forecast_pos_list)) {
                        continue;
                    }

                    float v_S = forecast_and_update(poly_id, OILS[poly_id], forecast_pos_list, max_v_S, best_oil_pos_list);

                    judge.forecasted_poly_set[poly_id].insert(Coordinate(base_y, base_x));
                    if (judge_if_turn_over()) {
                        return oil_pos_set;
                    }

                    FloatCoordinatePair pair = make_tuple(v_S, Coordinate(base_y,base_x));
                    research_pos_list[poly_id].push_back(pair);
                }
            }
        }

        // 付近に油田がある可能性が高いマス周辺を再占い
        for (int poly_id = 0; poly_id < M; ++poly_id) {
            sort(research_pos_list[poly_id].rbegin(), research_pos_list[poly_id].rend());
            for (int j = 0; j < min(int(research_pos_list[poly_id].size()), RESEARCH_TOP_K); ++j) {
                int base_y = get<1>(research_pos_list[poly_id][j]).y;
                int base_x = get<1>(research_pos_list[poly_id][j]).x;

                for (const auto& move : MOVE_AROUND) {
                    int ny = base_y + move.y;
                    int nx = base_x + move.x;

                    if (judge.forecasted_poly_set[poly_id].count(Coordinate(ny,nx)) > 0) {
                        continue;
                    }

                    auto forecast_pos_list = calc_forecast_pos_list(ny, nx, OILS[poly_id]);
                    if (forecast_pos_list.size() == 0) {
                        continue;
                    }
                    forecast_and_update(poly_id, OILS[poly_id], forecast_pos_list, max_v_S, best_oil_pos_list);
                    judge.forecasted_poly_set[poly_id].insert(Coordinate(ny,nx));

                    if (judge_if_turn_over()) {
                        return oil_pos_set;
                    }
                }
            }
        }

        for (const auto& oil_pos_list : best_oil_pos_list) {
            oil_pos_set.insert(oil_pos_list.begin(), oil_pos_list.end());
        }

        return oil_pos_set;
    }

    // N*Nの島全体をFORECAST_LEN*FORECAST_LENの座標グループに区切ってそれぞれの埋蔵量を占う
    void forecast_all_group(int forecast_len, int shift_num) {
        int forecast_group_len = (N + forecast_len - 1) / forecast_len;
        
        // より正確なv(S)が測れるように1マスずつ縦横をずらして複数回測定も可能
        for (int diff = 0; diff < shift_num; ++diff) {
            for (int gr_y = 0; gr_y < forecast_group_len; ++gr_y) {
                for (int gr_x = 0; gr_x < forecast_group_len; ++gr_x) {
                    vector<Coordinate> pos_list;
                    for (int dy = 0; dy < forecast_len; ++dy) {
                        for (int dx = 0; dx < forecast_len; ++dx) {
                            int y = forecast_len * gr_y + dy + diff;
                            int x = forecast_len * gr_x + dx + diff;
                            if (0 <= y && y < N && 0 <= x && x < N) {
                                pos_list.push_back({y, x});
                            }
                        }
                    }

                    // 占うためには2マス以上必要
                    if (pos_list.size() >= 2) {
                        judge.forecast_pos_list(pos_list);
                        // 上限ターンに達したら終了
                        if (judge_if_turn_over()) {
                            return;
                        }
                    }
                }
            }
        }
    }

    // 未占いマス(値が-1.0)の値を隣接マスの平均で補間する。
    void interpolate_unforecast_v_S() {
        while (true) {
            int cnt_unforecast_pos = 0;

            for (int y = 0; y < N; ++y) {
                for (int x = 0; x < N; ++x) {
                    if (judge.oil_forecast_map[y][x] == -1.0) {
                        float interpolate_v_S = 0;
                        int cnt = 0;
                        for (const auto& move : MOVE) {
                            int ny = y + move.y;
                            int nx = x + move.x;
                            if (0 <= ny && ny < N && 0 <= nx && nx < N && judge.oil_forecast_map[ny][nx] != -1.0) {
                                interpolate_v_S += judge.oil_forecast_map[ny][nx];
                                ++cnt;
                            }
                        }

                        if (cnt > 0) {
                            judge.oil_forecast_map[y][x] = float(interpolate_v_S / cnt);
                        } else {
                            ++cnt_unforecast_pos;
                        }
                    }
                }
            }

            if (cnt_unforecast_pos == 0) {
                break;
            }
        }
        return;
    }

    // 試し掘りの候補座標選定のため、占い結果の全座標をスコアが高い順になるように管理する。
    void create_sorted_v_S_pos_list() {
        for (int y = 0; y < N; ++y) {
            for (int x = 0; x < N; ++x) {
                float v_S = judge.oil_forecast_map[y][x];
                FloatCoordinatePair pair = make_tuple(v_S, Coordinate(y,x));
                sorted_v_S_pos_list.push_back(pair);
            }
        }
        sort(sorted_v_S_pos_list.begin(), sorted_v_S_pos_list.end(), greater<>());
    }

    // 油田が見つかる可能性が高いマスをいくつか試し掘りし、配置判定の情報を増やす。
    void trial_dig() {
        int trial_dig_cnt = 0;
        int cur_y = -1, cur_x = -1;
        int pre_y = -1, pre_x = -1;
        while (trial_dig_cnt < TRIAL_DIG_NUM && !(judge_if_turn_over() || judge_if_digged_all())) {
            int dig_idx = -1; // 掘る対象のインデックス
            // 最初は先頭マスを掘る
            if (pre_y == -1 && pre_x == -1) {
                dig_idx = 0;
                auto [_, cur_pos] = sorted_v_S_pos_list[dig_idx];
                cur_y = cur_pos.y;
                cur_x = cur_pos.x;
            } else {
                // 推定v(S)の高い順に見ていってマンハッタン距離の閾値を超えるマスがあればそれを掘る                
                for (int i = 0; i < sorted_v_S_pos_list.size(); ++i) {
                    auto [v_S, pos] = sorted_v_S_pos_list[i];
                    float dist = abs(pos.y - pre_y) + abs(pos.x - pre_x);
                    // まだ掘り進められていないうちは全体を満遍なく掘りたい
                    if (judge.digged_oil_pos_set.size() < float(total_oil_amount) * 0.8) {
                        int undigged_cnt = 0;
                        for (const auto &[dy,dx] : MOVE) {
                            int ny = pos.y + dy;
                            int nx = pos.x + dx;
                            if (0 <= ny && ny < N && 0 <= nx && nx < N && judge.oil_map[ny][nx] == -1) {
                                undigged_cnt++;
                            }
                        }
                        // まだ周囲が掘られていないマスを優先する
                        if (undigged_cnt == 4) {
                            dist *= DIST_WEIGHT;
                        }
                    }else {
                        // 隣接マスにv(y,x)>0のマスがあるマスを優先(油田とそれ以外の境界を掘りたい)
                        for (const auto &[dy,dx] : MOVE) {
                            int ny = pos.y + dy;
                            int nx = pos.x + dx;
                            if (0 <= ny && ny < N && 0 <= nx && nx < N && judge.oil_map[ny][nx] > 0) {
                                dist *= DIST_WEIGHT;
                                break;
                            }
                        }
                    }
                    if (dist > DIST_THRESHOLD) {
                        dig_idx = i;
                        cur_y = pos.y;
                        cur_x = pos.x;
                        break;
                    }
                }
                // 距離の閾値を超えるマスが無かった場合はv(S)最大の要素を採用
                if (dig_idx == -1) {
                    dig_idx = 0;
                    cur_y = get<1>(sorted_v_S_pos_list[0]).y;
                    cur_x = get<1>(sorted_v_S_pos_list[0]).x;
                }            
            }
            // 既に掘っている場合はスキップ
            if (judge.oil_map[cur_y][cur_x] != -1) {
                sorted_v_S_pos_list.erase(sorted_v_S_pos_list.begin() + dig_idx);
                continue;
            }
            // 油田が存在すると確定している場合はスキップ
            if (!judge.definitive_poly_pos_map[cur_y][cur_x].empty()) {
                sorted_v_S_pos_list.erase(sorted_v_S_pos_list.begin() + dig_idx);
                continue;
            }
            judge.dig_pos(cur_y, cur_x);
            // 掘ったマスはリストから削除
            sorted_v_S_pos_list.erase(sorted_v_S_pos_list.begin() + dig_idx);
            if (judge_if_turn_over() || judge_if_digged_all()) {
                break;
            }
            trial_dig_cnt++;
            pre_y = cur_y;
            pre_x = cur_x;
        }
    }

    // 全ての油田が見つかるまで、既に掘ったマスの隣接マスを掘る
    void dig_adjacent_pos() {
        // 始点の候補を決める(まだ掘られておらず、近くにv(y,x)>0のマスがあり、未発掘の隣接マスが多い)
        vector<FloatCoordinatePair> dig_cand_pos_list;
        for (int y = 0; y < N; ++y) {
            for (int x = 0; x < N; ++x) {
                // 発掘済みのマスはスキップ
                if (judge.oil_map[y][x] != -1) {
                    continue;
                }
                float adjacent_digged_oil_cnt = 0;
                for (const auto& [dy, dx] : MOVE) {
                    int ny = y + dy;
                    int nx = x + dx;
                    if (0 <= ny && ny < N && 0 <= nx && nx < N && judge.oil_map[ny][nx] > 0) {
                        ++adjacent_digged_oil_cnt;
                    }
                }
                float score = (adjacent_digged_oil_cnt == 0) ? -judge.oil_forecast_map[y][x] : -4.0 / adjacent_digged_oil_cnt;
                FloatCoordinatePair pair = make_tuple(score, Coordinate(y,x));
                dig_cand_pos_list.push_back(pair);
            }
        }

        // adjacent_digged_cntが正かつ小さい値のものを始点にする
        if (dig_cand_pos_list.empty()) {
            return;
        }
        sort(dig_cand_pos_list.begin(), dig_cand_pos_list.end());

        // 決まった始点の隣接マスをBFSで探索
        queue<Coordinate> start_pos;
        int start_y, start_x;
        start_y = get<1>(dig_cand_pos_list[0]).y;
        start_x = get<1>(dig_cand_pos_list[0]).x;
        start_pos.push(Coordinate(start_y, start_x));
        while (!start_pos.empty()) {
            int y = start_pos.front().y;
            int x = start_pos.front().x;
            start_pos.pop();

            // 一度も掘られていないマスならば掘り、そうでない場合は確定済のv(S)を使用
            int v_S = 0;
            if (judge.oil_map[y][x] == -1) {
                v_S = judge.dig_pos(y, x);
                if (judge_if_turn_over() || judge_if_digged_all()) {
                    return;
                }
            } else {
                v_S = judge.oil_map[y][x];
            }
            if (v_S == 0) {
                continue;
            }

            for (const auto& [dy, dx] : MOVE) {
                int ny = y + dy;
                int nx = x + dx;
                if (0 <= ny && ny < N && 0 <= nx && nx < N && judge.oil_map[ny][nx] == -1) {
                    start_pos.push(Coordinate(ny,nx));
                }
            }
        }
    }

    // 現時点で分かっている試し掘り情報と矛盾せず、推定v(S)の合計が最大となるポリオミノの配置を探索する。
    // 1.v(y,x)が0→ポリオミノを置いてはいけない
    // 2.v(y,x)が1以上→v(y,x)個ちょうどのポリオミノが置かれていないといけない
    set<Coordinate> find_optimal_arrangement() {

        // ポリオミノを配置しようとしている場所に矛盾が無いか確認
        auto _judge_if_no_contradict = [&](const vector<vector<set<int>>>& estimate_poly_pos_map) -> bool {
            for (int y = 0; y < N; ++y) {
                for (int x = 0; x < N; ++x) {
                    // まだv(y,x)が確定していないマスはスキップ
                    if (judge.oil_map[y][x] == -1) {
                        continue;
                    }
                    // ポリオミノの置かれたor置かれていない個数が確定したv(y,x)と矛盾する場合は失敗
                    if (estimate_poly_pos_map[y][x].size() != static_cast<size_t>(judge.oil_map[y][x])) {
                        return false;
                    }
                }
            }
            return true;
        };

        // 未確定ポリオミノの推定v(S)及び始点座標をv(S)の降順ソート済み配列に格納
        auto _calc_probable_poly_arrangement = [&](void) -> vector<vector<FloatCoordinatePair>> {
            vector<vector<FloatCoordinatePair>> probable_poly_list(M);
            for (int base_y = 0; base_y < N; ++base_y) {
                for (int base_x = 0; base_x < N; ++base_x) {
                    for (int poly_id : judge.possible_poly_pos_map[base_y][base_x]) {
                        OIL oil = OILS[poly_id];
                        float estimated_v_S = 0;
                        int oil_pos_cnt = 0;
                        bool failure_flg = false;
                        for (const auto& [dy, dx] : oil.relative_pos_list) {
                            int ny = base_y + dy;
                            int nx = base_x + dx;
                            if (!(0 <= ny && ny < N && 0 <= nx && nx < N)) {
                                failure_flg = true;
                                break;
                            }
                            // ポリオミノを置くべき場所の埋蔵量が0の場合矛盾
                            if (judge.oil_map[ny][nx] == 0) {
                                failure_flg = true;
                                break;
                            }
                            if (judge.oil_map[ny][nx] > 0) {
                                oil_pos_cnt += 1;
                            }
                            estimated_v_S += judge.oil_forecast_map[ny][nx];
                        }
                        if (failure_flg) {
                            continue;
                        }
                        // TODO: 推定v(S)が小さいポリオミノ配置はスキップする枝刈り。消した方がいいかも
                        if (estimated_v_S < float(oil.n) / 4) {
                            continue;
                        }
                        FloatCoordinatePair pair = make_tuple(estimated_v_S, Coordinate(base_y,base_x));
                        probable_poly_list[poly_id].push_back(pair);
                    }
                }
            }
            for (int i = 0; i < M; ++i) {
                sort(probable_poly_list[i].begin(), probable_poly_list[i].end(), greater<>());
                // probable_poly_list[i] = probable_poly_list[i].size() > 30 ? vector<FloatCoordinatePair>(probable_poly_list[i].begin(), probable_poly_list[i].begin() + 30) : probable_poly_list[i];
            }

            return probable_poly_list;
        };

        // メイン処理
        // 現時点で確定している情報を基に、v(y,x)>0マスに置けるポリオミノIDを列挙
        vector<vector<vector<int>>> occupied_pos_map = vector<vector<vector<int>>>(N, vector<vector<int>>(N, vector<int>()));
        for (int base_y = 0; base_y < N; ++base_y) {
            for (int base_x = 0; base_x < N; ++base_x) {
                for (int poly_id : judge.possible_poly_pos_map[base_y][base_x]) {
                    OIL oil = OILS[poly_id];
                    for (const auto& [dy, dx] : oil.relative_pos_list) {
                        int ny = base_y + dy;
                        int nx = base_x + dx;
                        // v(y,x)>0マスに置けるならIDを追加
                        if (judge.oil_map[ny][nx] > 0) {
                            occupied_pos_map[ny][nx].push_back(poly_id);
                        }
                    }
                }
            }
        }

        // 一意に置き場所が確定できるポリオミノを探索
        // TODO: あるポリオミノの配置が確定することで他の配置も連鎖的に確定していく場合があるため変化がなくなるまでループしたいがバグ取れず
        for (int base_y = 0; base_y < N; ++base_y) {
            for (int base_x = 0; base_x < N; ++base_x) {
                // TODO: 本当は全可能性を試したいけどTLEするようなら制限を設ける
                for (int poly_id : judge.possible_poly_pos_map[base_y][base_x]) {
                    OIL oil = OILS[poly_id];
                    for (const auto& [dy, dx] : oil.relative_pos_list) {
                        int ny = base_y + dy;
                        int nx = base_x + dx;
                        // v(y,x)>0マスで置けるポリオミノIDの種類数とv(y,x)が一致していれば確定
                        // 同じ種類のポリオミノIDが複数回置ける場合を除外する必要があることに注意
                        set<int> vec2set(occupied_pos_map[ny][nx].begin(), occupied_pos_map[ny][nx].end());
                        if (judge.oil_map[ny][nx] > 0 && judge.oil_map[ny][nx] == occupied_pos_map[ny][nx].size() && 
                            occupied_pos_map[ny][nx].size() == vec2set.size()) {
                            judge.definitive_poly_id.insert(poly_id);
                            for (const auto& [dy, dx] : oil.relative_pos_list) {
                                int ny = base_y + dy;
                                int nx = base_x + dx;
                                judge.definitive_poly_pos_map[ny][nx].insert(poly_id);
                                judge.definitive_oil_pos_set.insert(Coordinate(ny,nx));
                            }
                            break;
                        }
                    }
                }
            }
        }
        // 配置を確定できたポリオミノがある場合はoccupied_pos_mapから当該poly_idを取り除く
        for (int y = 0; y < N; ++y) {
            for (int x = 0; x < N; ++x) {
                for (int poly_id : judge.definitive_poly_id) {
                    auto it = occupied_pos_map[y][x].begin();
                    while (it != occupied_pos_map[y][x].end()) {
                        if (*it == poly_id) {
                            it = occupied_pos_map[y][x].erase(it);
                        } else {
                            ++it;
                        }
                    }
                }
            }
        }

        // 未確定ポリオミノの推定v(S)及び始点座標を配列に格納
        vector<vector<FloatCoordinatePair>> probable_poly_list = _calc_probable_poly_arrangement();

        // 一意に確定したポリオミノの配置に加え、確定したとみなせるポリオミノも確定扱いすることで組合せ数を減らす
        vector<vector<set<int>>> current_definitive_poly_pos_map(N, vector<set<int>>(N));
        set<int> current_definitive_poly_id;
        current_definitive_poly_id.insert(judge.definitive_poly_id.begin(), judge.definitive_poly_id.end());
        vector<Coordinate> current_definitive_pos_list;

        // まずは実際に確定したポリオミノの情報をコピー
        for (int y = 0; y < N; ++y) {
            for (int x = 0; x < N; ++x) {
                if (!judge.definitive_poly_pos_map[y][x].empty()) {
                    current_definitive_poly_pos_map[y][x].insert(judge.definitive_poly_pos_map[y][x].begin(), judge.definitive_poly_pos_map[y][x].end());
                    current_definitive_pos_list.push_back(Coordinate(y, x));
                }
            }
        }

        // 配置の組合せが何通りあるかを計算し多すぎる場合はスキップ
        long long pattern_num = 1;
        for (int poly_id = 0; poly_id < M; ++poly_id) {
            if (current_definitive_poly_id.count(poly_id) > 0) {
                continue;
            }
            pattern_num *= probable_poly_list[poly_id].size();
            if (pattern_num >= DFS_LIMIT) {
                return set<Coordinate>();
            }
        }

        // 確定済及び確定とみなしたポリオミノの配置を基に、未確定ポリオミノの最適配置をDFSで全探索
        // TODO: 確定とみなしたポリオミノは現状入れていない
        vector<FloatCoordinateVecPair> best_poly_pos_list; // 矛盾なく配置できたポリオミノの座標組合せを降順ソートしたリスト
        vector<int> current_undefinitive_poly_id;
        for (int poly_id = 0; poly_id < M; ++poly_id) {
            if (current_definitive_poly_id.count(poly_id) == 0) {
                current_undefinitive_poly_id.push_back(poly_id);
            }
        }

        // DFS
        auto search_best_poly_pos_dfs = [&](auto search_best_poly_pos_dfs, int i, int total_v_S, vector<vector<set<int>>>& current_definitive_poly_pos_map) -> void {
            // TLE対策
            cur_time = get_time(start_time);
            if (cur_time >= TIME_LIMIT) {
                return;
            }

            // 最後まで矛盾なく配置できたらtotal_v_Sと配置を記録
            if (i == current_undefinitive_poly_id.size()) {
                if (_judge_if_no_contradict(current_definitive_poly_pos_map)) {
                    vector<Coordinate> final_pos_list = current_definitive_pos_list;
                    for (int y = 0; y < N; ++y) {
                        for (int x = 0; x < N; ++x) {
                            if (!current_definitive_poly_pos_map[y][x].empty()) {
                                final_pos_list.emplace_back(y,x);
                            }
                        }
                    }
                    sort(final_pos_list.begin(), final_pos_list.end());
                    FloatCoordinateVecPair pair = make_tuple(total_v_S, move(final_pos_list));
                    best_poly_pos_list.push_back(pair);
                }
                return;
            }

            // probable_poly_listの上位から順に組合せを試す
            int poly_id = current_undefinitive_poly_id[i];
            const auto& oil = OILS[poly_id];
            for (const auto& [estimated_v_S, base_pos] : probable_poly_list[poly_id]) {
                set<Coordinate> pos_set;
                bool failure_flg = false;
                for (const auto& [dy, dx] : oil.relative_pos_list) {
                    int ny = base_pos.y + dy;
                    int nx = base_pos.x + dx;
                    // 仮にポリオミノを置いた(+1)場合に、確定済v(y,x)の値を超える場合は矛盾
                    if (judge.oil_map[ny][nx] != -1 && current_definitive_poly_pos_map[ny][nx].size() + 1 > judge.oil_map[ny][nx]) {
                        failure_flg = true;
                        break;
                    }
                    pos_set.emplace(ny, nx);
                }
                if (failure_flg) {
                    continue;
                }
                // 問題なければestimate_poly_pos_mapにpoly_idを追加して次のpoly_idの探索へ
                for (const auto& [y, x] : pos_set) {
                    current_definitive_poly_pos_map[y][x].insert(poly_id);
                }
                search_best_poly_pos_dfs(search_best_poly_pos_dfs, i+1, total_v_S+estimated_v_S, current_definitive_poly_pos_map);
                // 後処理
                for (const auto& [y, x] : pos_set) {
                    current_definitive_poly_pos_map[y][x].erase(poly_id);
                }
            }
        };

        search_best_poly_pos_dfs(search_best_poly_pos_dfs, 0, 0, current_definitive_poly_pos_map);
        sort(best_poly_pos_list.begin(), best_poly_pos_list.end(), [](const FloatCoordinateVecPair& a, const FloatCoordinateVecPair& b) {
            return get<0>(a) > get<0>(b);
        });

        // 回答用の座標セットを作成
        if (!best_poly_pos_list.empty()) {
            set<Coordinate> poly_pos_set(get<1>(best_poly_pos_list[0]).begin(), get<1>(best_poly_pos_list[0]).end());
            if (!poly_pos_set.empty()) {
                return poly_pos_set;
            }
        }
        return set<Coordinate>();
    }

};

/*********************回答をここに記載*********************/
int Solver::solve() {

    // 1. Mの大小によって初期方針を変える
    if (M <= INI_SWITCH_M) {
        // 1-1. Mが2の時はポリオミノの形そのままにスライドさせて最もv(S)が大きくなったところを解とする
        set<Coordinate> oil_pos_set = slide_optimal_oil_pos();
        if (oil_pos_set.size()) {
                int finish_flg = judge.answer(oil_pos_set);
                if (finish_flg == 1) {
                    return 0;
                }
            }
    } else {
        // 1-2. N*Nの島全体をFORECAST_LEN*FORECAST_LENのグループに区切ってそれぞれの埋蔵量を占う
        forecast_all_group(FORECAST_LEN,1);
        if (judge_if_turn_over()) {
            return 0;
        }
    }        

    // 2. 未占いマスを隣接マスの値の平均で補間
    interpolate_unforecast_v_S();

    // 3. 占い結果の全座標を推定v(S)が高い順になるように管理する。
    create_sorted_v_S_pos_list();

    // 4. 試し掘りと隣接マス発掘を繰り返す
    double cur_time = 0.0;
    while (true) {

        cur_time = get_time(start_time);
        // TIME_LIMITを超えるか上限ターンに達するか全ての埋蔵石油が発掘できたら終了
        if (cur_time >= TIME_LIMIT || judge_if_turn_over() || judge_if_digged_all()) {
            break;
        }

        // 4-1. 確定情報を増やすために試し掘りする
        if (judge.turn < TRIAL_DIG_SWITCH_TURN) {
            trial_dig();
        } else {
            for (int i = 0; i < TRIAL_DIG_NUM; ++i) {
                dig_adjacent_pos();
                if (judge_if_turn_over() || judge_if_digged_all()) {
                    break;
                }
            }
        }

        // 4-2. 現時点の情報を基に、最適な配置をDFSで探索し回答する
        auto oil_pos_set = find_optimal_arrangement();
        if (!oil_pos_set.empty()) {
            bool finish_flg = judge.answer(oil_pos_set);
            if (finish_flg) {
                return 0;
            }
        }
    }

    // # 5. ここまでに回答できていなければ全ての油田を発掘して答えを出力する
    while (!(judge_if_turn_over() || judge_if_digged_all())) {
        dig_adjacent_pos();
    }

    if (!judge_if_turn_over()) {
        // judge.digged_oil_pos_set.insert(judge.definitive_oil_pos_set.begin(), judge.definitive_oil_pos_set.end());
        judge.answer(judge.digged_oil_pos_set);
    }
    return 0;
}

int main() {
    int N, M;
    float EPS;
    cin >> N >> M >> EPS;

    vector<OIL> OILS;
    for (int i = 0; i < M; ++i) {
        int n;
        cin >> n;
        vector<Coordinate> absolute_pos_list;
        for (int j = 0; j < n; ++j) {
            int y, x;
            cin >> y >> x;
            absolute_pos_list.push_back(Coordinate(y, x));
        }
        vector<Coordinate> relative_pos_list;
        int base_y = absolute_pos_list[0].y;
        int base_x = absolute_pos_list[0].x;
        for (const auto& pos : absolute_pos_list) {
            int rel_y = pos.y - base_y;
            int rel_x = pos.x - base_x;
            relative_pos_list.push_back(Coordinate(rel_y, rel_x));
        }
        OILS.push_back(OIL(n, absolute_pos_list, relative_pos_list));
    }

    Solver solver(N, M, EPS, OILS);
    solver.solve();

    return 0;
}