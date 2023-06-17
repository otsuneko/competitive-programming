import sys
import time
import random
from collections import defaultdict

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

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return len(self.roots())

    def all_group_members(self):
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find(member)].append(member)
        return group_members

    def __str__(self):
        return '\n'.join(f'{r}: {m}' for r, m in self.all_group_members().items())

#クラスカル法
# V: 頂点集合(リスト) E: 辺集合[始点, 終点, 重み](リスト)
class kruskal():
    
    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.E.sort(key=lambda x: x[2]) #辺の重みでソート

    def weight(self): #最小全域木の重み和と選択された頂点を求める
        UF = UnionFind(len(self.V)) #頂点数でUnion Find Treeを初期化
        weight = 0
        nodes = set()
        edges = set()
        for i in range(len(self.E)):
            s,t,w,id = self.E[i]
            if not UF.same(s,t):
                UF.union(s,t)
                weight += w
                nodes.add(s)
                nodes.add(t)
                edges.add(id)

        return weight, sorted(list(nodes)), sorted(list(edges))

# 定数
TLE = 2.0

# 辺のOn/Offの初期値を決める
def create_ini_OnOff(broadcast_pos,edges):
    edges_flg = [0]*M

    mst = kruskal(broadcast_pos,edges)
    weight,min_nodes,min_edges = mst.weight()
    for id in min_edges:
        edges_flg[id] = 1
    return edges_flg[:]

# 辺のOn/Offを基に到達可能な放送局を返す
def get_reachable_broadcaster(edges,edges_flg):
    uf = UnionFind(N)
    for i in range(M):
        if edges_flg[i] == 1:
            uf.union(edges[i][0],edges[i][1])

    broadcast_list = uf.members(0)
    return broadcast_list

# 放送が届いている住民のリストを返す
def get_broadcasted_residents(broadcast_pos, broadcast_list, residents_pos,power):
    seen = set()
    remained_residents = set([i for i in range(K)])
    for id in broadcast_list:
        if len(seen) == K:
            break
        for k in list(remained_residents):
            bx,by = broadcast_pos[id]
            rx,ry = residents_pos[k]
            dist = (bx-rx)**2 + (by-ry)**2

            if dist <= power[id]**2:
                seen.add(k)
        remained_residents -= seen

    return sorted(list(seen))

# スコア計算
def calc_score(broadcasted_residents,cost):
    score = 0
    n = len(broadcasted_residents)
    # 全住民に放送できていない場合
    if n < K:
        score = round(10**6 * (n+1) / K)
    elif n == K:
        score = round(10**6 * (1 + 10**8 / (cost+10**7)))
    return score

# コスト計算
def calc_cost(edges,edges_flg,power):
    cost = 0
    for i in range(N):
        cost += power[i]**2

    for i in range(M):
        if edges_flg[i] == 1:
            cost += edges[i][2]
    
    return cost

# 計測開始
start = time.time()

# 入力
N,M,K = map(int,input().split())
broadcast_pos = [list(map(int,input().split())) for _ in range(N)]
edges = []
for id in range(M):
    u,v,w = map(int,input().split())
    u,v = u-1,v-1
    edges.append((u,v,w,id))

residents_pos = [list(map(int,input().split())) for _ in range(K)]

# 出力用変数の初期化
edges_flg = create_ini_OnOff(broadcast_pos, edges)
power = [2500]*N

# スコア改善ループ
final_score = 0
final_edges_flg = edges_flg[:]
final_power = power[:]
loop = 0
while 1:

    # TLE対策
    now = time.time()
    if now - start > TLE * 0.85:
        break

    # 山登りor焼きなましによる辺の修正、パワー改善
    # ランダムに選んだ辺のOn/Offを反転
    # rand_edge_id = random.randint(0,M-1)
    # if 0 not in edges[rand_edge_id][:2]:
    #     edges_flg[rand_edge_id] = (edges_flg[rand_edge_id] + 1) % 2

    # 放送が届く住民の数計算
    broadcast_list = get_reachable_broadcaster(edges, edges_flg)
    broadcasted_residents = get_broadcasted_residents(broadcast_pos, broadcast_list, residents_pos, power)

    # コスト計算
    cost = calc_cost(edges,edges_flg,power)
    
    # スコア計算
    score = calc_score(broadcasted_residents,cost)

    # パラメータ更新
    if score > final_score:
        final_score = score
        final_edges_flg = edges_flg[:]
        final_power = power[:]
    else:
        edges_flg = final_edges_flg[:]
        power = final_power[:]

    # print(loop, file=sys.stderr)
    loop += 1

print(*final_power)
print(*final_edges_flg)
print("N,M,K = ",N,M,K, file=sys.stderr)
print("score = ",final_score, file=sys.stderr)


