#include <cassert>
#include <cmath>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <climits>
#include <map>
#include <queue>
#include <set>
#include <cstring>
#include <vector>

using namespace std;
typedef long long ll;
typedef pair<int, int> P;

const int INF = INT_MAX;
const ll CYCLE_PER_SEC = 2700000000;
ll g_start_cycle;
double BUILD_TIME_LIMIT = 1.7;
double TIME_LIMIT = 0.4;

unsigned long long xor128() {
  static unsigned long long rx = 123456789, ry = 362436069, rz = 521288629, rw = 88675123;
  unsigned long long rt = (rx ^ (rx << 11));
  rx = ry;
  ry = rz;
  rz = rw;
  return (rw = (rw ^ (rw >> 19)) ^ (rt ^ (rt >> 8)));
}

unsigned long long int get_cycle() {
  unsigned int low, high;
  __asm__ volatile ("rdtsc" : "=a" (low), "=d" (high));
  return ((unsigned long long int) low) | ((unsigned long long int) high << 32);
}

double get_time(unsigned long long int begin_cycle) {
  return (double) (get_cycle() - begin_cycle) / CYCLE_PER_SEC;
}

const int TILE_TYPE_NUM = 16;
const int MAX_N = 10;
const int MAX_NODE_NUM = 100000;
int BLOCK_SIZE = 10;
const int LOOP_SIZE = 150;
const int GRID_SIZE = MAX_N + 2;
const int UNDEFINED = -1;
const int EMPTY_TYPE = 0;
const int LEFT = 0;
const int UP = 1;
const int RIGHT = 2;
const int DOWN = 3;
const string DS[4] = {"L", "U", "R", "D"};
const string DC[TILE_TYPE_NUM] = {" ", "→", "↓", "┘", "←", "─", "└", "┴", "↑", "┐", "│", "┤", "┌", "┬", "├", "┼"};
const int DY[4] = {0, -1, 0, 1};
const int DX[4] = {-1, 0, 1, 0};
const int DZ[4] = {-1, -GRID_SIZE, 1, GRID_SIZE};
int DBZ[4] = {-1, -BLOCK_SIZE, 1, BLOCK_SIZE};

int N, T;
char g_grid[GRID_SIZE * GRID_SIZE];
char g_origin_grid[GRID_SIZE * GRID_SIZE];
bool g_is_connect[TILE_TYPE_NUM][TILE_TYPE_NUM][4];
int g_tile_ids[GRID_SIZE * GRID_SIZE];
ll g_visited[GRID_SIZE * GRID_SIZE];
ll g_vid;
ll g_zobrist_hash[GRID_SIZE * GRID_SIZE][GRID_SIZE * GRID_SIZE];
int g_near_distance[GRID_SIZE * GRID_SIZE][TILE_TYPE_NUM];
bool g_can_not_place_tile[GRID_SIZE * GRID_SIZE][TILE_TYPE_NUM];
int LINE_BONUS = 10;
int BROKE_PENALTY = 1;
int CONFLICT_PENALTY = 4;
int SWAP_PENALTY = 4;

int calc_z(int y, int x) {
  return y * GRID_SIZE + x;
}

int calc_block_z(int y, int x) {
  return y * BLOCK_SIZE + x;
}

ll calc_tile_ids_hash() {
  ll hash = 0;

  for (int y = 1; y <= N; ++y) {
    for (int x = 1; x <= N; ++x) {
      int z = calc_z(y, x);
      int id = g_tile_ids[z];
      hash ^= g_zobrist_hash[z][id];
    }
  }

  return hash;
}

vector<int> clean_path(vector<int> &path) {
  vector<int> new_path;

  for (int dir : path) {
    if (new_path.size() > 0) {
      int last_dir = new_path.back();
      if (last_dir != dir && last_dir % 2 == dir % 2) {
        new_path.pop_back();
      } else {
        new_path.push_back(dir);
      }
    } else {
      new_path.push_back(dir);
    }
  }

  return new_path;
}

string path2str(vector<int> &path) {
  string res = "";

  for (int dir : path) {
    res += DS[dir];
  }

  return res;
}


struct Edge {
  int to;
  int cap;
  int rev;
  double cost;

  Edge(int to = -1, int cap = -1, int rev = -1, double cost = 0) {
    this->to = to;
    this->cap = cap;
    this->rev = rev;
    this->cost = cost;
  }
};

struct Config {
  int beam_width_1;
  int beam_width_2;
  int beam_width_3;
  int beam_width_4;
  int beam_width_5;

  Config() {
    this->beam_width_1 = 4000;
    this->beam_width_2 = 3000;
    this->beam_width_3 = 2000;
    this->beam_width_4 = 1000;
    this->beam_width_5 = 500;
  }
};

Config config;

struct Node {
  int id;
  int pid;
  int z;
  int last_dir;
  double value;
  double penalty;
  int board_value;
  double bonus;
  ll hash;
  char tile_ids[10 * 10];
  unsigned char path[LOOP_SIZE];

  Node(int id = -1, int pid = -1, int z = -1, int last_dir = -1, double value = 0.0, double penalty = 0.0) {
    this->id = id;
    this->pid = pid;
    this->z = z;
    this->last_dir = last_dir;
    this->value = value;
    this->penalty = penalty;
    this->bonus = 0;
  }

  bool operator>(const Node &n) const {
    return value - board_value + penalty - bonus > n.value - n.board_value + n.penalty - n.bonus;
  }

  void show_tile_ids() {
    for (int y = 0; y < BLOCK_SIZE; ++y) {
      for (int x = 0; x < BLOCK_SIZE; ++x) {
        int z = calc_block_z(y, x);
        int id = tile_ids[z];

        fprintf(stderr, "%4d", id);
      }
      fprintf(stderr, "\n");
    }
  }

  ll calc_hash() {
    ll hash = 0;

    for (int y = 0; y < BLOCK_SIZE; ++y) {
      for (int x = 0; x < BLOCK_SIZE; ++x) {
        int z = calc_block_z(y, x);
        int id = tile_ids[z];
        if (id < 0) continue;
        hash ^= g_zobrist_hash[z][id];
      }
    }

    return hash;
  }
};

struct NodeLight {
  int pid;
  int z;
  int last_dir;
  int bonus;
  double value;
  double penalty;
  int board_value;
  ll hash;

  NodeLight(int pid = -1, int z = -1, int last_dir = -1, double value = 0.0, double penalty = 0.0) {
    this->pid = pid;
    this->z = z;
    this->last_dir = last_dir;
    this->value = value;
    this->penalty = penalty;
    this->bonus = 0;
  }

  bool operator>(const NodeLight &n) const {
    return value - board_value + penalty - bonus > n.value - n.board_value + n.penalty - n.bonus;
  }
};

Node g_nodes[2][MAX_NODE_NUM];

class UnionFind {
public:
  vector<int> _parent;
  vector<int> _rank;
  vector<int> _size;

  UnionFind(int n) {
    for (int i = 0; i < n; ++i) {
      _parent.push_back(i);
      _rank.push_back(0);
      _size.push_back(1);
    }
  }

  int find(int x) {
    if (_parent[x] == x) {
      return x;
    } else {
      return _parent[x] = find(_parent[x]);
    }
  }

  void unite(int x, int y) {
    x = find(x);
    y = find(y);
    if (x == y) return;

    if (_rank[x] < _rank[y]) {
      _parent[x] = y;
      _size[y] += _size[x];
    } else {
      _parent[y] = x;
      _size[x] += _size[y];
      if (_rank[x] == _rank[y]) ++_rank[x];
    }
  }

  bool same(int x, int y) {
    return find(x) == find(y);
  }

  int size(int x) {
    return _size[find(x)];
  }
};

class MinCostFlow {
public:
  int V;
  vector<int> h;
  vector<double> dist;
  vector<int> prevv;
  vector<int> preve;
  vector <vector<Edge>> G;

  MinCostFlow(int V) {
    this->V = V;
    h.resize(V);
    dist.resize(V);
    prevv.resize(V);
    preve.resize(V);
    G.resize(V);
  }

  void add_edge(int from, int to, int cap, int cost) {
    G[from].push_back(Edge(to, cap, G[to].size(), cost));
    G[to].push_back(Edge(from, 0, G[from].size() - 1, -cost));
  }

  double min_cost_flow(int s, int t, int flow_limit) {
    int f = 0;
    ll total_cost = 0;
    fill(h.begin(), h.end(), 0);

    while (f < flow_limit) {
      // fprintf(stderr, "f: %d, limit: %d\n", f, flow_limit);
      priority_queue <P, vector<P>, greater<P>> pque;
      fill(dist.begin(), dist.end(), INF);
      dist[s] = 0;
      pque.push(P(0, s));

      while (!pque.empty()) {
        P p = pque.top();
        pque.pop();
        int v = p.second;
        if (dist[v] < p.first) continue;

        for (int i = 0; i < (int) G[v].size(); ++i) {
          Edge *edge = &G[v][i];
          if (edge->cap <= 0) continue;

          ll cost = edge->cost + h[v] - h[edge->to];
          if (dist[edge->to] - dist[v] > cost) {
            dist[edge->to] = dist[v] + cost;
            prevv[edge->to] = v;
            preve[edge->to] = i;
            pque.push(P(dist[edge->to], edge->to));
          }
        }
      }

      if (dist[t] == INF) {
        return -1;
      }

      for (int v = 0; v < V; ++v) {
        h[v] += dist[v];
      }

      int c = flow_limit - f;
      for (int v = t; v != s; v = prevv[v]) {
        c = min(c, G[prevv[v]][preve[v]].cap);
      }

      f += c;
      total_cost += c * h[t];

      // fprintf(stderr, "h[s]: %d, h[t]: %d, cost: %d, prev_cost: %d\n", h[s], h[t], cost, prev_cost);

      for (int v = t; v != s; v = prevv[v]) {
        Edge *edge = &G[prevv[v]][preve[v]];
        edge->cap -= c;
        G[v][edge->rev].cap += c;
      }
    }

    return total_cost;
  }
};

class SlidingTreePuzzle {
public:
  void init() {
    memset(g_grid, UNDEFINED, sizeof(g_grid));
    memset(g_visited, 0, sizeof(g_visited));
    memset(g_tile_ids, UNDEFINED, sizeof(g_tile_ids));

    g_vid = 0;
  }

  void load_data() {
    fprintf(stderr, "load_data =>\n");
    cin >> N >> T;
    fprintf(stderr, "N = %d\n", N);

    for (int y = 1; y <= N; ++y) {
      string row;
      cin >> row;

      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);
        char ch = row[x - 1];
        int type;

        if (ch <= '9') {
          type = ch - '0';
        } else {
          type = ch - 'a' + 10;
        }

        g_grid[z] = type;
      }
    }

    BLOCK_SIZE = min(N, BLOCK_SIZE);
    BROKE_PENALTY = 1;
    CONFLICT_PENALTY = 2 * BROKE_PENALTY;
    SWAP_PENALTY = 4 * CONFLICT_PENALTY;
    DBZ[1] = -BLOCK_SIZE;
    DBZ[3] = BLOCK_SIZE;
    memcpy(g_origin_grid, g_grid, sizeof(g_grid));
  }

  void restore() {
    memcpy(g_grid, g_origin_grid, sizeof(g_origin_grid));
  }

  void setup() {
    fprintf(stderr, "setup =>\n");
    setup_is_connect();
    setup_zobrist_hash();
    setup_near_distance();
    setup_can_not_place_tile();
  }

  void setup_can_not_place_tile() {
    memset(g_can_not_place_tile, false, sizeof(g_can_not_place_tile));

    for (int y = 1; y <= N; ++y) {
      int lz = calc_z(y, 1);
      int rz = calc_z(y, N);

      for (int t = 1; t < TILE_TYPE_NUM; ++t) {
        if (t >> LEFT & 1) {
          g_can_not_place_tile[lz][t] = true;
        }
        if (t >> RIGHT & 1) {
          g_can_not_place_tile[rz][t] = true;
        }
      }
    }

    for (int x = 1; x <= N; ++x) {
      int uz = calc_z(1, x);
      int dz = calc_z(N, x);

      for (int t = 1; t < TILE_TYPE_NUM; ++t) {
        if (t >> UP & 1) {
          g_can_not_place_tile[uz][t] = true;
        }
        if (t >> DOWN & 1) {
          g_can_not_place_tile[dz][t] = true;
        }
      }
    }
  }

  void setup_near_distance() {
    memset(g_near_distance, 0, sizeof(g_near_distance));
    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);

        for (int t = 0; t < TILE_TYPE_NUM; ++t) {
          g_near_distance[z][t] = INT_MAX;
        }
      }
    }
    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);
        int type = g_origin_grid[z];

        for (int y2 = 1; y2 <= N; ++y2) {
          for (int x2 = 1; x2 <= N; ++x2) {
            int z2 = calc_z(y2, x2);
            int dist = calc_my_md(abs(y - y2), abs(x - x2));

            g_near_distance[z2][type] = min(g_near_distance[z2][type], dist);
          }
        }
      }
    }
  }

  void setup_zobrist_hash() {
    for (int y = 0; y < GRID_SIZE; ++y) {
      for (int x = 0; x < GRID_SIZE; ++x) {
        int z = calc_z(y, x);

        for (int y = 0; y < GRID_SIZE; ++y) {
          for (int x = 0; x < GRID_SIZE; ++x) {
            int id = calc_z(y, x);
            g_zobrist_hash[z][id] = xor128();
          }
        }
      }
    }
  }

  void setup_is_connect() {
    memset(g_is_connect, false, sizeof(g_is_connect));

    for (int i = 0; i < TILE_TYPE_NUM; ++i) {
      for (int j = 0; j < TILE_TYPE_NUM; ++j) {
        for (int dir = 0; dir < 4; ++dir) {
          switch (dir) {
            case 0:
              if ((i & 1) && (j & 4)) {
                g_is_connect[i][j][dir] = true;
              }
              break;
            case 1:
              if ((i & 2) && (j & 8)) {
                g_is_connect[i][j][dir] = true;
              }
              break;
            case 2:
              if ((i & 4) && (j & 1)) {
                g_is_connect[i][j][dir] = true;
              }
              break;
            case 3:
              if ((i & 8) && (j & 2)) {
                g_is_connect[i][j][dir] = true;
              }
              break;
          }
        }
      }
    }
  }

  vector<int> run() {
    init();
    load_data();
    setup();

    g_start_cycle = get_cycle();
    double cur_time = get_time(g_start_cycle);

    int min_diff = INT_MAX;
    int best_ids[GRID_SIZE * GRID_SIZE];
    memset(best_ids, UNDEFINED, sizeof(best_ids));
    int cnt = 0;
    double val = 1.0;

    while (cur_time < BUILD_TIME_LIMIT && cnt < 15) {
      restore();
      cur_time = get_time(g_start_cycle);
      double remain_time = min(BUILD_TIME_LIMIT - cur_time, TIME_LIMIT);
      if (not build_mst_by_sa(remain_time, val)) {
        val += 1.0;
        continue;
      }

      val = max(0.0, val - 1.0);

      ++cnt;
      int lim = 10;
      map<ll, bool> checked;

      for (int j = 0; j < lim && cur_time < BUILD_TIME_LIMIT; ++j) {
        int diff = assign_tile_number_flow();
        if (not can_complete_puzzle()) {
          continue;
        }
        ll hash = calc_tile_ids_hash();
        if (checked[hash]) continue;
        checked[hash] = true;

        if (min_diff > diff) {
          min_diff = diff;
          memcpy(best_ids, g_tile_ids, sizeof(g_tile_ids));
        }

        cur_time = get_time(g_start_cycle);
      }

      if (min_diff != INT_MAX) {
        // NOOP
      } else {
        val += 1.0;
      }

      cur_time = get_time(g_start_cycle);
    }

    fprintf(stderr, "try_count: %d, val: %f\n", cnt, val);
    memcpy(g_tile_ids, best_ids, sizeof(best_ids));
    // show_tile_number();

    vector<int> build_path;
    memcpy(g_grid, g_origin_grid, sizeof(g_origin_grid));
    // show_grid();

    cur_time = get_time(g_start_cycle);

    while (cur_time < 3.0) {
      vector<int> res = search_tile_move_path(1, 1, N, N);
      fprintf(stderr, "size: %d\n", (int) res.size());
      if (res.empty()) break;
      build_path.insert(build_path.end(), res.begin(), res.end());

      int ez = find_empty_tile_pos();
      for (int dir : res) {
        assert(0 <= dir && dir <= 3);
        int nz = ez + DZ[dir];
        int ny = nz / GRID_SIZE;
        int nx = nz % GRID_SIZE;
        assert(1 <= ny && ny <= N);
        assert(1 <= nx && nx <= N);
        swap(g_grid[ez], g_grid[nz]);
        swap(g_tile_ids[ez], g_tile_ids[nz]);
        ez = nz;
      }
      // show_grid();
    }

    return build_path;
  }

  int calc_my_md(int dy, int dx) {
    return dy * dy + dx * dx;
  }

  int find_empty_tile_pos() {
    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);
        if (g_grid[z] == EMPTY_TYPE) return z;
      }
    }

    fprintf(stderr, "Not found empty tile\n");
    show_grid();
    assert(false);
  }

  Node build_root_node(int sy, int sx, int ty, int tx) {
    Node node(0);
    memset(node.tile_ids, UNDEFINED, sizeof(node.tile_ids));
    memset(node.path, 0, sizeof(node.path));

    for (int y = sy; y <= ty; ++y) {
      for (int x = sx; x <= tx; ++x) {
        int z = calc_z(y, x);
        int nz = calc_block_z(y - sy, x - sx);
        int tid = g_tile_ids[z];
        int ty = tid / GRID_SIZE;
        int tx = tid % GRID_SIZE;
        int n_tid = calc_block_z(ty - sy, tx - sx);
        assert(0 <= nz && nz < BLOCK_SIZE * BLOCK_SIZE);
        node.tile_ids[nz] = n_tid;
      }
    }

    int ez = find_empty_tile_pos();
    int ey = ez / GRID_SIZE;
    int ex = ez % GRID_SIZE;
    node.z = calc_block_z(ey - sy, ex - sx);
    fprintf(stderr, "oe: (%d, %d), e: (%d, %d)\n", ez / GRID_SIZE, ez % GRID_SIZE, ey - sy, ex - sx);
    node.tile_ids[node.z] = -1;
    assert(0 <= node.z && node.z < BLOCK_SIZE * BLOCK_SIZE);
    node.hash = node.calc_hash();
    node.penalty = calc_full_linear_conflict(node) + calc_full_neighbor_cnt(node);
    node.board_value = calc_board_value_full(node);

    return node;
  }

  void setup_search_config() {
    if (N == 10) {
      config.beam_width_1 = 1000;
      config.beam_width_2 = 1000;
      config.beam_width_3 = 1000;
    } else if (N == 9) {
      config.beam_width_1 = 2000;
      config.beam_width_2 = 2000;
      config.beam_width_3 = 2000;
    } else if (N == 8) {
      config.beam_width_1 = 3000;
      config.beam_width_2 = 3000;
      config.beam_width_3 = 2000;
      config.beam_width_4 = 1000;
    } else if (N == 7) {
      config.beam_width_1 = 4000;
      config.beam_width_2 = 3000;
      config.beam_width_3 = 3000;
      config.beam_width_4 = 2000;
      config.beam_width_5 = 1000;
    } else {
      config.beam_width_1 = 6000;
      config.beam_width_2 = 6000;
      config.beam_width_3 = 4000;
      config.beam_width_4 = 4000;
      config.beam_width_5 = 1000;
    }
  }

  vector<int> search_tile_move_path(int sy = 1, int sx = 1, int ty = N, int tx = N) {
    queue<int> que;
    setup_search_config();
    Node root = build_root_node(sy, sx, ty, tx);
    root.value = calc_estimate(root);
    assert(root.id == 0);
    g_nodes[0][root.id] = root;
    que.push(root.id);

    vector<int> best_path;
    int beam_width = config.beam_width_1;
    map<ll, bool> checked;

    if (root.value <= 0) {
      return best_path;
    }

    for (int depth = 0; depth < 4 * LOOP_SIZE && que.size() > 0; ++depth) {
      // fprintf(stderr, "depth: %d, size: %d\n", depth, (int) que.size());
      priority_queue <NodeLight, vector<NodeLight>, greater<NodeLight>> pque;
      double cur_time = get_time(g_start_cycle);
      if (cur_time >= 1.9) beam_width = config.beam_width_2;
      if (cur_time >= 2.25) beam_width = config.beam_width_3;
      if (cur_time >= 2.5) beam_width = config.beam_width_4;
      if (cur_time >= 2.7) beam_width = config.beam_width_5;

      while (not que.empty()) {
        int nid = que.front();
        Node &node = g_nodes[depth % 2][nid];
        int y = node.z / BLOCK_SIZE;
        int x = node.z % BLOCK_SIZE;
        assert(0 <= node.z && node.z < BLOCK_SIZE * BLOCK_SIZE);
        que.pop();

        int cache_board_score[4];
        cache_board_score[0] = calc_board_value_left_to_right(node);
        cache_board_score[1] = calc_board_value_right_to_left(node);
        cache_board_score[2] = calc_board_value_up_to_down(node);
        cache_board_score[3] = calc_board_value_down_to_up(node);

        for (int dir = 0; dir < 4; ++dir) {
          if ((node.last_dir ^ 2) == dir) continue;

          int ny = y + DY[dir];
          int nx = x + DX[dir];
          if (ny < 0 || nx < 0 || ny >= BLOCK_SIZE || nx >= BLOCK_SIZE) continue;
          int nz = calc_block_z(ny, nx);

          NodeLight next(node.id, nz, dir, node.value, node.penalty);
          next.hash = node.hash;
          next.hash ^= g_zobrist_hash[nz][(int) node.tile_ids[nz]];
          next.value -= calc_md(node, nz);
          next.penalty -= calc_linear_conflict(node, nz);
          next.penalty -= calc_neighbor_cnt(node, nz);
          next.bonus = calc_bonus(node, nz);
          next.board_value = node.board_value;

          swap(node.tile_ids[node.z], node.tile_ids[nz]);

          switch (dir) {
            case UP:
              if (ny < (N - 2) / 2) {
                next.board_value -= cache_board_score[2];
                next.board_value += calc_board_value_up_to_down(node);
              }
              if (y >= BLOCK_SIZE - (N - 2) / 2) {
                next.board_value -= cache_board_score[3];
                next.board_value += calc_board_value_down_to_up(node);
              }
              break;
            case DOWN:
              if (y < (N - 2) / 2) {
                next.board_value -= cache_board_score[2];
                next.board_value += calc_board_value_up_to_down(node);
              }
              if (ny >= BLOCK_SIZE - (N - 2) / 2) {
                next.board_value -= cache_board_score[3];
                next.board_value += calc_board_value_down_to_up(node);
              }
              break;
            case LEFT:
              if (nx < (N - 2) / 2) {
                next.board_value -= cache_board_score[0];
                next.board_value += calc_board_value_left_to_right(node);
              }
              if (x >= BLOCK_SIZE - (N - 2) / 2) {
                next.board_value -= cache_board_score[1];
                next.board_value += calc_board_value_right_to_left(node);
              }
              break;
            case RIGHT:
              if (x < (N - 2) / 2) {
                next.board_value -= cache_board_score[0];
                next.board_value += calc_board_value_left_to_right(node);
              }
              if (nx >= BLOCK_SIZE - (N - 2) / 2) {
                next.board_value -= cache_board_score[1];
                next.board_value += calc_board_value_right_to_left(node);
              }
              break;
          }

          if (node.board_value - next.board_value < LINE_BONUS) {
            next.hash ^= g_zobrist_hash[node.z][(int) node.tile_ids[node.z]];
            next.value += calc_md(node, node.z);
            next.penalty += calc_linear_conflict(node, node.z);
            next.penalty += calc_neighbor_cnt(node, node.z);
            pque.push(next);
          }
          swap(node.tile_ids[node.z], node.tile_ids[nz]);
        }
      }

      if (not pque.empty() && depth == 4 * LOOP_SIZE - 1) {
        NodeLight node = pque.top();
        Node &parent = g_nodes[depth % 2][node.pid];
        unsigned char path[LOOP_SIZE];
        memcpy(path, parent.path, sizeof(parent.path));
        int idx = depth / 4;
        int sec = depth % 4;
        path[idx] = path[idx] | (node.last_dir << (2 * sec));

        vector<int> res;
        for (int j = 0; j <= depth; ++j) {
          int idx = j / 4;
          int sec = j % 4;
          int dir = (path[idx] >> (2 * sec)) & 3;
          assert(0 <= dir && dir <= 3);
          res.push_back(dir);
        }
        best_path = res;
      }

      for (int i = 0; i < beam_width && not pque.empty(); ++i) {
        NodeLight l_node = pque.top();
        pque.pop();

        if (checked[l_node.hash]) {
          --i;
          continue;
        }
        checked[l_node.hash] = true;

        Node &parent = g_nodes[depth % 2][l_node.pid];
        int id = (depth % 2 == 0) ? i + 10000 : i;
        Node &node = g_nodes[(depth + 1) % 2][id];
        node.id = id;
        node.pid = l_node.pid;
        node.z = l_node.z;
        node.last_dir = l_node.last_dir;
        node.value = l_node.value;
        node.penalty = l_node.penalty;
        node.board_value = l_node.board_value;
        node.hash = l_node.hash;
        memcpy(node.tile_ids, parent.tile_ids, sizeof(parent.tile_ids));
        memcpy(node.path, parent.path, sizeof(parent.path));
        int z = node.z + DBZ[node.last_dir ^ 2];
        assert(0 <= z && z < BLOCK_SIZE * BLOCK_SIZE);
        int idx = depth / 4;
        int sec = depth % 4;
        node.path[idx] = node.path[idx] | (node.last_dir << (2 * sec));
        swap(node.tile_ids[z], node.tile_ids[node.z]);

        if (node.value <= 0) {
          vector<int> res;
          for (int j = 0; j <= depth; ++j) {
            int idx = j / 4;
            int sec = j % 4;
            int dir = (node.path[idx] >> (2 * sec)) & 3;
            assert(0 <= dir && dir <= 3);
            res.push_back(dir);
          }
          return res;
        }

        g_nodes[(depth + 1) % 2][id] = node;
        que.push(id);
      }
    }

    return best_path;
  }

  int calc_estimate(Node &node) {
    int value = 0;

    for (int y = 0; y < BLOCK_SIZE; ++y) {
      for (int x = 0; x < BLOCK_SIZE; ++x) {
        int z = calc_block_z(y, x);
        int id = node.tile_ids[z];
        if (id == -1) continue;

        value += calc_md(node, z);
      }
    }

    return value;
  }

  int calc_full_linear_conflict(Node &node) {
    int penalty = 0;

    for (int y = 0; y < BLOCK_SIZE; ++y) {
      for (int x = 0; x < BLOCK_SIZE - 1; ++x) {
        int z1 = calc_block_z(y, x);
        int z2 = calc_block_z(y, x + 1);
        int id1 = node.tile_ids[z1];
        int id2 = node.tile_ids[z2];
        if (id1 < 0) continue;
        if (id2 < 0) continue;
        int iy1 = id1 / BLOCK_SIZE;
        int ix1 = id1 % BLOCK_SIZE;
        int iy2 = id2 / BLOCK_SIZE;
        int ix2 = id2 % BLOCK_SIZE;
        if (ix1 > ix2) penalty += BROKE_PENALTY;
        if (ix1 < ix2) penalty -= BROKE_PENALTY;
        if (z1 == id2 && iy1 == iy2 && id1 > id2) penalty += CONFLICT_PENALTY;
        if (z2 == id1 && iy1 == iy2 && id1 > id2) penalty += CONFLICT_PENALTY;
        if (z1 == id2 && z2 == id1) penalty += SWAP_PENALTY;
      }
    }

    for (int y = 0; y < BLOCK_SIZE - 1; ++y) {
      for (int x = 0; x < BLOCK_SIZE; ++x) {
        int z1 = calc_block_z(y, x);
        int z2 = calc_block_z(y + 1, x);
        int id1 = node.tile_ids[z1];
        int id2 = node.tile_ids[z2];
        if (id1 < 0) continue;
        if (id2 < 0) continue;
        int iy1 = id1 / BLOCK_SIZE;
        int ix1 = id1 % BLOCK_SIZE;
        int iy2 = id2 / BLOCK_SIZE;
        int ix2 = id2 % BLOCK_SIZE;
        if (iy1 > iy2) penalty += BROKE_PENALTY;
        if (iy1 < iy2) penalty -= BROKE_PENALTY;
        if (z1 == id2 && ix1 == ix2 && id1 > id2) penalty += CONFLICT_PENALTY;
        if (z2 == id1 && ix1 == ix2 && id1 > id2) penalty += CONFLICT_PENALTY;
        if (z1 == id2 && z2 == id1) penalty += SWAP_PENALTY;
      }
    }

    return penalty;
  }

  int calc_linear_conflict(Node &node, int z) {
    int penalty = 0;
    int y = z / BLOCK_SIZE;
    int x = z % BLOCK_SIZE;
    int id1 = node.tile_ids[z];
    int iy1 = id1 / BLOCK_SIZE;
    int ix1 = id1 % BLOCK_SIZE;
    assert(id1 != -1);

    for (int dir = 0; dir < 4; ++dir) {
      int ny = y + DY[dir];
      int nx = x + DX[dir];
      if (ny < 0 || nx < 0 || ny >= BLOCK_SIZE || nx >= BLOCK_SIZE) continue;
      int nz = calc_block_z(ny, nx);
      int id2 = node.tile_ids[nz];
      if (id2 < 0) continue;
      int iy2 = id2 / BLOCK_SIZE;
      int ix2 = id2 % BLOCK_SIZE;

      if (dir == LEFT) {
        if (ix2 < ix1) penalty -= BROKE_PENALTY;
        if (ix2 > ix1) penalty += BROKE_PENALTY;
        if (iy1 == iy2) {
          if (z == id2 && id1 < id2) penalty += CONFLICT_PENALTY;
          if (nz == id1 && id1 < id2) penalty += CONFLICT_PENALTY;
        }
      }
      if (dir == UP) {
        if (iy2 < iy1) penalty -= BROKE_PENALTY;
        if (iy2 > iy1) penalty += BROKE_PENALTY;
        if (ix1 == ix2) {
          if (z == id2 && id1 < id2) penalty += CONFLICT_PENALTY;
          if (nz == id1 && id1 < id2) penalty += CONFLICT_PENALTY;
        }
      }
      if (dir == RIGHT) {
        if (ix1 < ix2) penalty -= BROKE_PENALTY;
        if (ix1 > ix2) penalty += BROKE_PENALTY;
        if (iy1 == iy2) {
          if (z == id2 && id1 > id2) penalty += CONFLICT_PENALTY;
          if (nz == id1 && id1 > id2) penalty += CONFLICT_PENALTY;
        }
      }
      if (dir == DOWN) {
        if (iy1 < iy2) penalty -= BROKE_PENALTY;
        if (iy1 > iy2) penalty += BROKE_PENALTY;
        if (ix1 == ix2) {
          if (z == id2 && id1 > id2) penalty += CONFLICT_PENALTY;
          if (nz == id1 && id1 > id2) penalty += CONFLICT_PENALTY;
        }
      }

      if (z == id2 && nz == id1) penalty += SWAP_PENALTY;
    }

    return penalty;
  }

  double calc_bonus(Node &node, int z) {
    double bonus = 0;
    int y = z / BLOCK_SIZE;
    int x = z % BLOCK_SIZE;

    for (int dir = 0; dir < 4; ++dir) {
      int ny = y + DY[dir];
      int nx = x + DX[dir];
      if (ny < 0 || nx < 0 || ny >= BLOCK_SIZE || nx >= BLOCK_SIZE) continue;
      int nz = calc_block_z(ny, nx);
      int id = node.tile_ids[nz];
      if (id < 0) continue;
      int iy = id / BLOCK_SIZE;
      int ix = id % BLOCK_SIZE;
      int dy_new = abs(iy - y);
      int dy_old = abs(iy - ny);
      int dx_new = abs(ix - x);
      int dx_old = abs(ix - nx);

      const double B1 = 0.5;
      if (dir == LEFT && dx_old > dx_new) bonus += B1 * (dx_old * dx_old - dx_new * dx_new);
      if (dir == RIGHT && dx_old > dx_new) bonus += B1 * (dx_old * dx_old - dx_new * dx_new);
      if (dir == UP && dy_old > dy_new) bonus += B1 * (dy_old * dy_old - dy_new * dy_new);
      if (dir == DOWN && dy_old > dy_new) bonus += B1 * (dy_old * dy_old - dy_new * dy_new);
    }

    return bonus;
  }

  int calc_full_neighbor_cnt(Node &node) {
    int penalty = 0;

    for (int y = 0; y < BLOCK_SIZE; ++y) {
      for (int x = 0; x < BLOCK_SIZE - 1; ++x) {
        int z1 = calc_block_z(y, x);
        int z2 = calc_block_z(y, x + 1);

        int id1 = node.tile_ids[z1];
        if (id1 < 0) continue;
        int iy1 = id1 / BLOCK_SIZE;
        int ix1 = id1 % BLOCK_SIZE;
        if (abs(y - iy1) + abs(x - ix1) >= 2) continue;

        int id2 = node.tile_ids[z2];
        if (id2 < 0) continue;
        int iy2 = id2 / BLOCK_SIZE;
        int ix2 = id2 % BLOCK_SIZE;
        if (abs(y - iy2) + abs((x + 1) - ix2) >= 2) continue;

        if (abs(iy1 - iy2) + abs(ix1 - ix2) <= 1) penalty -= 1;
      }
    }

    for (int y = 0; y < BLOCK_SIZE - 1; ++y) {
      for (int x = 0; x < BLOCK_SIZE; ++x) {
        int z1 = calc_block_z(y, x);
        int z2 = calc_block_z(y + 1, x);

        int id1 = node.tile_ids[z1];
        if (id1 < 0) continue;
        int iy1 = id1 / BLOCK_SIZE;
        int ix1 = id1 % BLOCK_SIZE;
        if (abs(y - iy1) + abs(x - ix1) >= 2) continue;

        int id2 = node.tile_ids[z2];
        if (id2 < 0) continue;
        int iy2 = id2 / BLOCK_SIZE;
        int ix2 = id2 % BLOCK_SIZE;
        if (abs((y + 1) - iy2) + abs(x - ix2) >= 2) continue;

        if (abs(iy1 - iy2) + abs(ix1 - ix2) <= 1) penalty -= 1;
      }
    }

    return penalty;
  }

  int calc_neighbor_cnt(Node &node, int z) {
    int penalty = 0;
    int y = z / BLOCK_SIZE;
    int x = z % BLOCK_SIZE;
    int id1 = node.tile_ids[z];
    assert(id1 != -1);

    for (int dir = 0; dir < 4; ++dir) {
      int ny = y + DY[dir];
      int nx = x + DX[dir];
      if (ny < 0 || nx < 0 || ny >= BLOCK_SIZE || nx >= BLOCK_SIZE) continue;
      int nz = calc_block_z(ny, nx);
      int id2 = node.tile_ids[nz];
      if (id2 < 0) continue;

      int iy1 = id1 / BLOCK_SIZE;
      int ix1 = id1 % BLOCK_SIZE;
      if (abs(y - iy1) + abs(x - ix1) >= 2) continue;

      int iy2 = id2 / BLOCK_SIZE;
      int ix2 = id2 % BLOCK_SIZE;
      if (abs(ny - iy2) + abs(nx - ix2) >= 2) continue;

      if (abs(iy1 - iy2) + abs(ix1 - ix2) <= 1) penalty -= 1;
    }

    return penalty;
  }

  int calc_board_value_full(Node &node) {
    int val = 0;

    val += calc_board_value_left_to_right(node);
    val += calc_board_value_right_to_left(node);
    val += calc_board_value_up_to_down(node);
    val += calc_board_value_down_to_up(node);

    return val;
  }

  int calc_board_value_left_to_right(Node &node) {
    int val = 0;

    bool ok = true;
    for (int x = 0; x < (N - 2) / 2 && ok; ++x) {
      for (int y = 0; y < BLOCK_SIZE && ok; ++y) {
        int z = calc_block_z(y, x);
        ok &= (node.tile_ids[z] == z);
      }

      if (ok) val += LINE_BONUS;
    }

    return val;
  }

  int calc_board_value_right_to_left(Node &node) {
    int val = 0;
    bool ok = true;

    for (int x = BLOCK_SIZE - 1; x >= BLOCK_SIZE - (N - 2) / 2 && ok; --x) {
      for (int y = 0; y < BLOCK_SIZE && ok; ++y) {
        int z = calc_block_z(y, x);
        ok &= (node.tile_ids[z] == z);
      }

      if (ok) val += LINE_BONUS;
    }

    return val;
  }

  int calc_board_value_up_to_down(Node &node) {
    int val = 0;
    bool ok = true;

    for (int y = 0; y < (N - 2) / 2; ++y) {
      for (int x = 0; x < BLOCK_SIZE && ok; ++x) {
        int z = calc_block_z(y, x);
        ok &= (node.tile_ids[z] == z);
      }

      if (ok) val += LINE_BONUS;
    }

    return val;
  }

  int calc_board_value_down_to_up(Node &node) {
    int val = 0;
    bool ok = true;

    for (int y = BLOCK_SIZE - 1; y >= BLOCK_SIZE - (N - 2) / 2; --y) {
      for (int x = 0; x < BLOCK_SIZE && ok; ++x) {
        int z = calc_block_z(y, x);
        ok &= (node.tile_ids[z] == z);
      }

      if (ok) val += LINE_BONUS;
    }

    return val;
  }

  int calc_md(Node &node, int z) {
    assert(0 <= z && z < BLOCK_SIZE * BLOCK_SIZE);
    int y = z / BLOCK_SIZE;
    int x = z % BLOCK_SIZE;
    int id = node.tile_ids[z];
    assert(0 <= id && id < BLOCK_SIZE * BLOCK_SIZE);
    int iy = id / BLOCK_SIZE;
    int ix = id % BLOCK_SIZE;

    return pow(abs(iy - y), 2) + pow(abs(ix - x), 2);
  }

  bool can_complete_puzzle() {
    vector<int> S(GRID_SIZE * GRID_SIZE);
    int ey, ex, ty, tx;
    vector<int> ZS;

    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);

        if (g_origin_grid[z] == EMPTY_TYPE) {
          ey = y;
          ex = x;
        }
        if (g_grid[z] == EMPTY_TYPE) {
          ty = y;
          tx = x;
        }

        ZS.push_back(z);
        S[z] = g_tile_ids[z];
      }
    }

    UnionFind uf(GRID_SIZE * GRID_SIZE);
    for (int v : ZS) {
      int u = S[v];
      uf.unite(u, v);
    }

    bool checked[GRID_SIZE * GRID_SIZE];
    memset(checked, false, sizeof(checked));
    int switch_cnt = 0;
    for (int u : ZS) {
      int x = uf.find(u);
      if (checked[x]) continue;
      checked[x] = true;

      switch_cnt += uf.size(x) - 1;
    }

    int e_dist = abs(ey - ty) + abs(ex - tx);

    return switch_cnt % 2 == e_dist % 2;
  }

  int assign_tile_number_flow() {
    int V = 2 * GRID_SIZE * GRID_SIZE + 2;
    MinCostFlow mcf(V);
    int s = 2 * (GRID_SIZE * GRID_SIZE);
    int t = 2 * (GRID_SIZE * GRID_SIZE) + 1;
    int G = GRID_SIZE * GRID_SIZE;

    for (int y1 = 1; y1 <= N; ++y1) {
      for (int x1 = 1; x1 <= N; ++x1) {
        int z1 = calc_z(y1, x1);
        int c_type = g_origin_grid[z1];
        mcf.add_edge(s, z1, 1, 0);
        mcf.add_edge(z1 + G, t, 1, 0);

        for (int y2 = 1; y2 <= N; ++y2) {
          for (int x2 = 1; x2 <= N; ++x2) {
            int z2 = calc_z(y2, x2);
            int type = g_grid[z2];
            if (c_type != type) continue;

            int dy = abs(y1 - y2);
            int dx = abs(x1 - x2);
            int md = dy * dy + dx * dx;
            int my = max(y1, N - y1 + 1);
            int mx = max(x1, N - x1 + 1);
            md *= max(my, mx);
            md += xor128() % N;

            mcf.add_edge(z1, z2 + G, 1, md);
          }
        }
      }
    }

    int total_md = 0;
    double res = mcf.min_cost_flow(s, t, N * N);
    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);

        for (Edge &e : mcf.G[z]) {
          if (e.to == s) continue;
          if (e.cap > 0) continue;
          int gz = e.to - G;

          total_md += e.cost;
          g_tile_ids[z] = gz;
          assert(g_origin_grid[z] == g_grid[gz]);
        }
      }
    }

    return total_md;
  }

  bool build_mst_by_sa(double time_limit, double val = 0) {
    memcpy(g_grid, g_origin_grid, sizeof(g_origin_grid));
    ll start_cycle = get_cycle();

    int ez = find_empty_tile_pos();
    int mz = calc_z(N / 2 + 1, N / 2 + 1);
    swap(g_grid[ez], g_grid[mz]);

    int cc_penalty = N * N * N * (1 + val);
    int cur_score = cc_penalty * lake_count();
    char cur_grid[GRID_SIZE * GRID_SIZE];
    memcpy(cur_grid, g_grid, sizeof(g_grid));

    int min_score = cur_score;
    int min_lc = INT_MAX;
    double cur_time = get_time(start_cycle);
    int try_count = 0;
    double total_diff = 0.0;
    double t = 3.0;
    int R = 500000;
    int n_value = 0;

    vector<int> ZS;
    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);
        int type = g_grid[z];
        ZS.push_back(z);

        n_value += g_near_distance[z][type];
      }
    }

    cur_score += n_value;
    min_score = cur_score;
    int L = ZS.size();

    int z1, z2;
    int no_cnt = 0;
    while (cur_time < time_limit && min_lc >= 3) {
      cur_time = get_time(start_cycle);
      double remain_time = (time_limit - cur_time) / time_limit;

      do {
        z1 = ZS[xor128() % L];
      } while (g_grid[z1] == EMPTY_TYPE);

      do {
        z2 = ZS[xor128() % L];
      } while (z1 == z2 || g_grid[z2] == EMPTY_TYPE || g_grid[z1] == g_grid[z2]);

      int t1 = g_grid[z1];
      int t2 = g_grid[z2];

      if (g_can_not_place_tile[z1][t2]) continue;
      if (g_can_not_place_tile[z2][t1]) continue;

      bool ok1 = false;
      for (int dir = 0; dir < 4 && not ok1; ++dir) {
        int nz = z1 + DZ[dir];
        int type = g_grid[nz];
        if (type == UNDEFINED) continue;
        if (g_is_connect[t2][type][dir]) ok1 = true;
      }

      bool ok2 = false;
      for (int dir = 0; dir < 4 && not ok2; ++dir) {
        int nz = z2 + DZ[dir];
        int type = g_grid[nz];
        if (type == UNDEFINED) continue;
        if (g_is_connect[t1][type][dir]) ok2 = true;
      }

      if (not ok1 && not ok2) continue;
      int temp = n_value;
      n_value -= (g_near_distance[z1][t1] + g_near_distance[z2][t2]);
      swap(g_grid[z1], g_grid[z2]);
      n_value += (g_near_distance[z2][t1] + g_near_distance[z1][t2]);
      int lc = lake_count();
      int score = cc_penalty * lc + n_value;
      double diff_score = cur_score - score;
      total_diff += fabs(diff_score);

      if (diff_score > 0 || (xor128() % R < R * exp(diff_score / (t * sqrt(remain_time))))) {
        cur_score = score;

        if (min_score > score) {
          min_lc = min(min_lc, lc);
          min_score = score;
          memcpy(cur_grid, g_grid, sizeof(g_grid));
          no_cnt = 0;
        }
      } else {
        ++no_cnt;
        swap(g_grid[z1], g_grid[z2]);
        n_value = temp;
      }

      ++try_count;
      double average_diff = total_diff / try_count;
      t = 0.005 * remain_time * average_diff;
      if (no_cnt >= 100000) break;
    }

    memcpy(g_grid, cur_grid, sizeof(cur_grid));

    return min_lc <= 2;
  }

  int lake_count() {
    int cnt = 0;
    ++g_vid;

    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int cz = calc_z(y, x);
        if (g_visited[cz] == g_vid) continue;

        ++cnt;
        dfs(cz);
      }
    }

    return cnt;
  }

  void dfs(int z) {
    g_visited[z] = g_vid;
    int c_type = g_grid[z];

    for (int dir = 0; dir < 4; ++dir) {
      int nz = z + DZ[dir];
      int type = g_grid[nz];
      if (type == UNDEFINED) continue;
      if (not g_is_connect[c_type][type][dir]) continue;
      if (g_visited[nz] == g_vid) continue;

      dfs(nz);
    }
  }

  void show_grid() {
    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);
        int type = g_grid[z];

        if (type == UNDEFINED) {
          fprintf(stderr, "x ");
        } else if (type == EMPTY_TYPE) {
          fprintf(stderr, ". ");
        } else {
          fprintf(stderr, "%s ", DC[type].c_str());
        }
      }
      fprintf(stderr, "\n");
    }
  }

  void show_tile_number() {
    for (int y = 1; y <= N; ++y) {
      for (int x = 1; x <= N; ++x) {
        int z = calc_z(y, x);

        fprintf(stderr, "%4d", g_tile_ids[z]);
      }
      fprintf(stderr, "\n");
    }
  }
};

int main() {
  SlidingTreePuzzle stp;
  ll start_cycle = get_cycle();
  vector<int> res = stp.run();
  vector<int> new_path = clean_path(res);

  fprintf(stderr, "path_size: (%d -> %d)\n", (int) res.size(), (int) new_path.size());
  string ans = path2str(new_path);

  double time = get_time(start_cycle);
  if (time > 3.0) {
    fprintf(stderr, "over time!!\n");
  }
  int L = ans.size();
  int score = ceil(500000 * (2 - L * 1.0 / T));
  fprintf(stderr, "Score = %d\n", score);
  fprintf(stderr, "L: (%d/%d), time: %f\n", L, T, time);
  // cerr << ans << endl;
  cout << ans << endl;

  return 0;
}