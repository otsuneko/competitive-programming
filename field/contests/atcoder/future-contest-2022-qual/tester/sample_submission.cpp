#include <cassert>
#include <cmath>
#include <iostream>
#include <utility>
#include <vector>

using namespace std;

const int DR[4] = {1, 0, -1, 0};
const int DC[4] = {0, 1, 0, -1};

struct Vegetable {
    int r, c, s, e, v;
    Vegetable(int r_, int c_, int s_, int e_, int v_)
     : r(r_), c(c_), s(s_), e(e_), v(v_) {
    }
};

struct Action {
    vector<int> vs;

private:
    explicit Action(const vector<int>& vs_) : vs(vs_) {}

public:
    static Action pass() {
        return Action({-1});
    }

    static Action purchase(int r, int c) {
        return Action({r, c});
    }

    static Action move(int r1, int c1, int r2, int c2) {
        return Action({r1, c1, r2, c2});
    }
};

int N, M, T;
vector<vector<Vegetable>> veges_start; // veges_start[i] : vegetables appear on day i
vector<vector<Vegetable>> veges_end;   // veges_end[i] : vegetables disappear on day i

struct Game {
    vector<vector<int>> has_machine;
    vector<vector<int>> vege_values;
    int num_machine;
    int next_price;
    int money;

    Game() : num_machine(0), next_price(1), money(1) {
        has_machine.assign(N, vector<int>(N, 0));
        vege_values.assign(N, vector<int>(N, 0));
    }

    void purchase(int r, int c) {
        assert(!has_machine[r][c]);
        assert(next_price <= money);
        has_machine[r][c] = 1;
        money -= next_price;
        num_machine++;
        next_price = (num_machine + 1) * (num_machine + 1) * (num_machine + 1);
    }

    void move(int r1, int c1, int r2, int c2) {
        assert(has_machine[r1][c1]);
        has_machine[r1][c1] = 0;
        assert(!has_machine[r2][c2]);
        has_machine[r2][c2] = 1;
    }

    void simulate(int day, const Action& action) {
        // apply
        if (action.vs.size() == 2) {
            purchase(action.vs[0], action.vs[1]);
        } else if (action.vs.size() == 4) {
            move(action.vs[0], action.vs[1], action.vs[2], action.vs[3]);
        }
        // appear
        for (const Vegetable& vege : veges_start[day]) {
            vege_values[vege.r][vege.c] = vege.v;
        }
        // harvest
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (has_machine[i][j] && vege_values[i][j] > 0) {
                    money += vege_values[i][j] * count_connected_machines(i, j);
                    vege_values[i][j] = 0;
                }
            }
        }
        // disappear
        for (const Vegetable& vege : veges_end[day]) {
            vege_values[vege.r][vege.c] = 0;
        }
    }

    int count_connected_machines(int r, int c) {
        vector<pair<int, int>> queue = {{r, c}};
        vector<vector<int>> visited(N, vector<int>(N, 0));
        visited[r][c] = 1;
        int i = 0;
        while (i < queue.size()) {
            int cr = queue[i].first;
            int cc = queue[i].second;
            for (int dir = 0; dir < 4; dir++) {
                int nr = cr + DR[dir];
                int nc = cc + DC[dir];
                if (0 <= nr && nr < N && 0 <= nc && nc < N && has_machine[nr][nc] && !visited[nr][nc]) {
                    visited[nr][nc] = 1;
                    queue.push_back({nr, nc});
                }
            }
            i++;
        }
        return i;
    }

    Action select_next_action(int day) {
        // implement your strategy here

        if (money < next_price) {
            return Action::pass();
        } else {
            // search best place for a new machine
            vector<vector<int>> sum_future_veges(N, vector<int>(N, 0));
            for (int i = day; i < T; i++) {
                for (const Vegetable& vege : veges_start[i]) {
                    sum_future_veges[vege.r][vege.c] += vege.v;
                }
            }
            int max_sum = 0;
            int max_r = -1;
            int max_c = -1;
            for (int r = 0; r < N; r++) {
                for (int c = 0; c < N; c++) {
                    if (has_machine[r][c]) {
                        continue;
                    }
                    if (max_sum < sum_future_veges[r][c]) {
                        max_sum = sum_future_veges[r][c];
                        max_r = r;
                        max_c = c;
                    }
                }
            }
            if (max_sum > 0) {
                return Action::purchase(max_r, max_c);
            } else {
                return Action::pass();
            }
        }
    }
};

int main() {
    cin >> N >> M >> T;
    veges_start.resize(T);
    veges_end.resize(T);
    for (int i = 0; i < M; i++) {
        int r, c, s, e, v;
        cin >> r >> c >> s >> e >> v;
        Vegetable vege(r, c, s, e, v);
        veges_start[s].push_back(vege);
        veges_end[e].push_back(vege);
    }
    Game game;
    vector<Action> actions;
    for (int day = 0; day < T; day++) {
        Action action = game.select_next_action(day);
        actions.push_back(action);
        game.simulate(day, action);
    }
    for (const Action& action : actions) {
        for (int i = 0; i < action.vs.size(); i++) {
            cout << action.vs[i] << (i == action.vs.size() - 1 ? "\n" : " ");
        }
    }
}
