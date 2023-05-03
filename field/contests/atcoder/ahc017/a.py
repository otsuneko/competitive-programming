import random
import time
from heapq import heappush, heappop
import sys
input = lambda: sys.stdin.readline().rstrip()

# 定数
INF=10**18
TIME_LIMIT = 6

# union-find木
class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1]*n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def size(self, x):
        return -self.parents[self.find(x)]

    def same(self, x, y):
        return self.find(x) == self.find(y)

# クラスカル法
# V: 頂点集合(リスト) E: 辺集合[始点, 終点, 重み](リスト)
class kruskal():
    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.E.sort(key=lambda x: x[3]) #辺の重みでソート

    def weight(self): #最小全域木の重み和と選択された頂点を求める
        UF = UnionFind(len(self.V)) #頂点数でUnion Find Treeを初期化
        weight = 0
        nodes = set()
        edges = set()
        for i in range(len(self.E)):
            i,s,t,w = self.E[i]
            if not UF.same(s,t):
                UF.union(s,t)
                weight += w
                nodes.add(s)
                nodes.add(t)
                edges.add((i,s,t,w))

        return weight, sorted(list(nodes)), edges

# ダイクストラ(最短経路導出用)
def dijkstra(d,s,prohibited):
    hq = [(0, s)] # (distance, node)
    while hq:
        cost,v = heappop(hq) # ノードを pop する
        if d[v] < cost:
            continue
        for i, to, cost in graph[v]: # ノード v に隣接しているノードに対して
            if i in prohibited:
                continue
            if d[v] + cost < d[to]:
                d[to] = d[v] + cost
                heappush(hq, (d[to], to))

# ある日の工事に対する不満度計算
def calc_complain_ratio(prohibited):
    total_dist_diff = 0 # 距離の差分の合計
    min_dist = [[10**9]*N for _ in range(N)]
    for s in range(N):
        dist = [10**9]*N
        dist[s] = 0
        dijkstra(dist,s,prohibited)
        for t in range(s+1,N):
            min_dist[s][t] = dist[t]
            total_dist_diff += min_dist[s][t] - min_dist_ori[s][t] if min_dist[s][t] != 10**9 else 10**9
    return total_dist_diff / (N*(N-1))

##########################################メイン処理##########################################
# 計測開始
start = time.time()

# 入力
N,M,D,K = map(int,input().split())
nodes = [0]*N
edges = []
graph = [[] for _ in range(N)]
for i in range(M):
    u,v,w = map(int,input().split())
    u,v = u-1,v-1
    graph[u].append((i,v,w))
    graph[v].append((i,u,w))
    edges.append((i,u,v,w))

# i 番目の頂点の座標(ビジュアライズ用のため解法には無関係)
pos = [list(map(int,input().split())) for _ in range(N)]

# 最小全域木を構築する辺の情報を前計算
mst = kruskal(nodes,edges)
mst_edges = mst.weight()[2]

# ダイクストラで、工事してない時の各頂点間の最短距離を計算
min_dist_ori = [[10**9]*N for _ in range(N)]
prohibited = set()
for s in range(N):
    dist = [10**9]*N
    dist[s] = 0
    dijkstra(dist,s,prohibited)
    for t in range(s+1,N):
        min_dist_ori[s][t] = dist[t]

# 一番工事がうまくいく順序をシミュレーションで求める
best_construction_order = []
for day in range(1,D+1):
    best_construction_order += [day]*K
best_construction_order = best_construction_order[:M]
min_complain_ratio = calc_complain_ratio(best_construction_order)
while 1:

    # TLE対策
    now = time.time()
    if now - start > TIME_LIMIT*0.8:
        break

    # ループ変数初期化
    tmp_mst_edges = set(list(mst_edges))
    tmp_other_edges = set(edges[:]) - tmp_mst_edges
    constructed_edges = set()
    construction_order = [0]*M
    total_complain_ratio = 0

    # 乱数シミュレーション
    for day in range(D):

        # TLE対策
        now = time.time()
        if now - start > TIME_LIMIT*0.8:
            break

        # 全ての辺が工事完了したら終了
        if len(tmp_mst_edges) == 0 and len(tmp_other_edges) == 0:
            break
        
        # MSTに含まれる辺1本とそれ以外の辺の合計construction_limit本を工事対象のprohibitedとして選択
        prohibited = set()
        # construction_limit = random.randint(int(K*0.9), K)
        construction_limit = K

        # MSTに含まれる辺
        num_sample_mst_edges = min(len(tmp_mst_edges), int((len(mst_edges)+D-1)//D*1.5))
        sample_mst_edges = random.sample(list(tmp_mst_edges), num_sample_mst_edges)
        for mst_edge in sample_mst_edges:
            tmp_mst_edges.remove(mst_edge)
            prohibited.add(mst_edge[0])

        # MSTに含まれない辺
        num_sample_other_edges = min(len(tmp_other_edges), construction_limit-num_sample_mst_edges)
        sample_other_edges = random.sample(list(tmp_other_edges), num_sample_other_edges)
        for other_edge in sample_other_edges:
            tmp_other_edges.remove(other_edge)
            prohibited.add(other_edge[0])

        # 工事中の辺をconstruction_orderに反映
        for i in prohibited:
            construction_order[i] = day+1
        
        # その日の工事の不満度を計算
        total_complain_ratio += calc_complain_ratio(prohibited)
    
    # TLE対策で途中breakした場合は出力に移行
    if len(tmp_mst_edges) != 0 or len(tmp_other_edges) != 0:
        continue
    
    # 不満度計算
    total_complain_ratio = round(10**3 * total_complain_ratio / D)

    if total_complain_ratio < min_complain_ratio:
        min_complain_ratio = total_complain_ratio
        best_construction_order = construction_order[:]

print(*best_construction_order)