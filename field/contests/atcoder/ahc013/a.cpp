#include <cassert>
#include <iostream>
#include <map>
#include <random>
#include <utility>
#include <vector>
#include <set>

using namespace std;

// N*Nのグリッド。
// グリッドの種類…0：何もない、1~5：PCがある、6~10：PC番号+5のケーブルが存在
// true：接続中、false：未接続
// 接続元PCの座標(boolがtrueの場合のみ使用)
// 接続先PCの座標(boolがtrueの場合のみ使用)

struct Status{
    int kind;
    bool isConnected;
    pair<int,int> from;
    pair<int,int> to;
};

typedef vector<vector<Status>> Field;

// ある座標から別の座標にコンピュータを移動する
struct MoveAction {
    int before_row, before_col, after_row, after_col;
    MoveAction(int before_row, int before_col, int after_row, int after_col) : 
        before_row(before_row), before_col(before_col), after_row(after_row), after_col(after_col) {}
};

// ある座標のコンピュータと縦横のいずれかが同じ座標にある別のコンピュータを接続する
struct ConnectAction {
    int c1_row, c1_col, c2_row, c2_col;
    ConnectAction(int c1_row, int c1_col, int c2_row, int c2_col) : 
        c1_row(c1_row), c1_col(c1_col), c2_row(c2_row), c2_col(c2_col) {}
};

// 結果格納用
struct Result {
    vector<MoveAction> move;
    vector<ConnectAction> connect;
    Result(const vector<MoveAction> &move, const vector<ConnectAction> &con) : move(move), connect(con) {}
};

// このコードの肝
struct Solver {
    static constexpr const char USED = 'x';
    static constexpr int DR[4] = {0, 1, 0, -1};
    static constexpr int DC[4] = {1, 0, -1, 0};

    int N, K;
    int action_count_limit; //行動回数制限(移動と接続の合計で、K*100)
    mt19937 engine; // 乱数生成用
    Field field; // N*Nのグリッド
    vector<string> ori_connect_field; // 移動無しで接続した世界のfield
    set<tuple<int,int,char>> computers; // コンピュータの情報(i,j,kind)

    // Solver構造体のコンストラクタ
    Solver(int N, int K, const vector<vector<tuple<int,bool,pair<int,int>,pair<int,int>>>> &field, int seed = 0) : 
        N(N), K(K), action_count_limit(K * 100), field(field)
    {
        engine.seed(seed);
    }

    // コンピュータの初期位置を格納
    void set_computer_position(set<tuple<int,int,char>> &computers){
        for (int i=0; i<N; i++) {
            for (int j=0; j<N; j++) {
                if (field[i][j] != '0') {
                    computers.insert(make_tuple(i,j,field[i][j]));
                }
            }
        }
    }

    // ある座標にあるコンピュータが指定した方向に移動できるかを判定
    bool can_move(int row, int col, int dir, vector<string> &field) const
    {
        int nrow = row + DR[dir];
        int ncol = col + DC[dir];
        if (0 <= nrow && nrow < N && 0 <= ncol && ncol < N) {
            return field[nrow][ncol] == '0';
        }
        return false;
    }

    // コンピュータの移動を決定
    // MEMO：方針として、周辺n近傍のマスを探索した時に縦横に自分と同種のコンピュータが少ないものを優先的に移動させる。
    vector<MoveAction> move(int move_limit, vector<string> &field)
    {
        vector<MoveAction> ret;
        if (move_limit == -1) {
            move_limit = K * 50;
        }

        // for (int i = 0; i < move_limit; i++) {
        //     int row = engine() % N;
        //     int col = engine() % N;
        //     int dir = engine() % 4;
        //     if (field[row][col] != '0' && can_move(row, col, dir)) {
        //         swap(field[row][col], field[row + DR[dir]][col + DC[dir]]);
        //         ret.emplace_back(row, col, row + DR[dir], col + DC[dir]);
        //         action_count_limit--;
        //     }
        // }

        return ret;
    }

    // あるコンピュータから見てdirの方向に接続可能なコンピュータがあるか判定(壁に当たらない&別のケーブルまたはコンピュータに当たらない)
    bool can_connect(int row, int col, int dir, vector<string> &field) const
    {
        int nrow = row + DR[dir];
        int ncol = col + DC[dir];
        while (0 <= nrow && nrow < N && 0 <= ncol && ncol < N) {
            if (field[nrow][ncol] == field[row][col]) {
                return true;
            } else if (field[nrow][ncol] != '0') {
                return false;
            }
            nrow += DR[dir];
            ncol += DC[dir];
        }
        return false;
    }

    // 接続元のコンピュータから接続先のコンピュータまでの直線を"×"にする
    ConnectAction line_fill(int row, int col, int dir, vector<string> &field)
    {
        int nrow = row + DR[dir];
        int ncol = col + DC[dir];
        while (0 <= nrow && nrow < N && 0 <= ncol && ncol < N) {
            if (field[nrow][ncol] == field[row][col]) {
                return ConnectAction(row, col, nrow, ncol);
            }
            assert(field[nrow][ncol] == '0');
            field[nrow][ncol] = USED;
            nrow += DR[dir];
            ncol += DC[dir];
        }
        assert(false);
    }

    // 接続元のコンピュータから接続先のコンピュータまでの直線を"×"にする
    vector<ConnectAction> connect(vector<string> &field)
    {
        vector<ConnectAction> ret;
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (field[i][j] != '0' && field[i][j] != 'x') {
                    for (int dir = 0; dir < 2; dir++) {
                        if (can_connect(i, j, dir, field)) {
                            ret.push_back(line_fill(i, j, dir, field));
                            action_count_limit--;
                            if (action_count_limit <= 0) {
                                return ret;
                            }
                        }
                    }
                }
            }
        }
        return ret;
    }

    // フィールド出力用
    void print_field(const vector<string> &field)
    {
        for (auto f : field) {
            cout << f << endl;
        }
    }

    // ソルバ構造体のメンバ関数を組み合わせて問題を解く部分
    Result solve()
    {
        // コンピュータの初期位置と種類を格納        
        set_computer_position(computers);

        // 移動せずに接続する用のフィールドを初期化
        ori_connect_field = field;
        // まず最初に何も移動しない状態で試しに繋いだことにしてみる
        auto tmp_connects = connect(ori_connect_field);
        // 再初期化
        action_count_limit = K * 100;

        // cout << "field" << endl;
        // print_field(field);
        // cout << "ori_connect_field" << endl;
        // print_field(ori_connect_field);

        // create random moves
        auto moves = move(-1, field);
        auto connects = connect(field);
        // from each computer, connect to right and/or bottom if it will reach the same type
        // auto connects = connect();
        return Result(moves, connects);
    }
};

struct UnionFind {
    map<pair<int,int>, pair<int, int>> parent;
    UnionFind() :parent() {}

    pair<int, int> find(pair<int, int> x)
    {
        if (parent.find(x) == parent.end()) {
            parent[x] = x;
            return x;
        } else if (parent[x] == x) {
            return x;
        } else {
            parent[x] = find(parent[x]);
            return parent[x];
        }
    }

    void unite(pair<int, int> x, pair<int, int> y)
    {
        x = find(x);
        y = find(y);
        if (x != y) {
            parent[x] = y;
        }
    }
};

// スコア計算用(Resultを基に、毎回計算)
// MEMO:スコアの差分計算による高速化ができる？
int calc_score(int N, Field field, const Result &res)
{
    // コンピュータの移動をシミュレート
    for (auto r : res.move) {
        assert(field[r.before_row][r.before_col].kind != 0);
        assert(field[r.after_row][r.after_col].kind == 0);
        swap(field[r.before_row][r.before_col].kind, field[r.after_row][r.after_col].kind);
    }

    // コンピュータの接続をシミュレート
    UnionFind uf;
    for (auto r : res.connect) {
        pair<int, int> p1(r.c1_row, r.c1_col), p2(r.c2_row, r.c2_col);
        uf.unite(p1, p2);
    }

    // コンピュータの座標を格納
    vector<pair<int, int>> computers;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (field[i][j].kind != 0) {
                computers.emplace_back(i, j);
            }
        }
    }

    // あるUFクラスタ内で同じ種類のコンピュータが接続なら+1点、違う種類のコンピュータが接続なら-1点
    // MEMO:基本的にUFクラスタを少なくしてなるべく同じ種類のPCを1クラスタにまとめるほうが、
    // 一部接続できないPCが出たとしてもトータルでスコアは上がるはず。
    int score = 0;
    for (int i = 0; i < (int)computers.size(); i++) {
        for (int j = i+1; j < (int)computers.size(); j++) {
            auto c1 = computers[i];
            auto c2 = computers[j];
            if (uf.find(c1) == uf.find(c2)) {
                score += (field[c1.first][c1.second].kind == field[c2.first][c2.second].kind) ? 1 : -1;
            }
        }
    }

    return max(score, 0);
}

// 結果出力用
void print_answer(const Result &res)
{
    cout << res.move.size() << endl;
    for (auto m : res.move) {
        cout << m.before_row << " " << m.before_col << " "
            << m.after_row << " " << m.after_col << endl;
    }
    cout << res.connect.size() << endl;
    for (auto m : res.connect) {
        cout << m.c1_row << " " << m.c1_col << " "
            << m.c2_row << " " << m.c2_col << endl;
    }
}

int main()
{
    int N, K;
    cin >> N >> K;
    Field field;
    for (int i = 0; i < N; i++) {
        string str;
        cin >> str;
        for (int j = 0; j < (int)str.size(); j++){
            field[i][j].kind = int(str[j]);
            field[i][j].isConnected = false;
            field[i][j].from = make_pair(-1,-1);
            field[i][j].to = make_pair(-1,-1);
        }
    }

    Solver s(N, K, field);
    auto ret = s.solve();

    cerr << "Score = " << calc_score(N, field, ret) << endl;

    print_answer(ret);

    return 0;
}
