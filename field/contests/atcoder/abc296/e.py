import sys
sys.setrecursionlimit(10**7)

# 強連結成分分解(SCC): グラフGに対するSCCを行う
# 入力: <N>: 頂点サイズ, <G>: 順方向の有向グラフ, <RG>: 逆方向の有向グラフ
# 出力: num_group:ラベル数, group:各頂点のラベル番号
def scc(N, G, RG):
    order = []
    used = [0]*N
    group = [None]*N
    def dfs(s):
        used[s] = 1
        for t in G[s]:
            if not used[t]:
                dfs(t)
        order.append(s)
    def rdfs(s, col):
        group[s] = col
        used[s] = 1
        for t in RG[s]:
            if not used[t]:
                rdfs(t, col)
    for i in range(N):
        if not used[i]:
            dfs(i)
    used = [0]*N
    num_group = 0
    for s in reversed(order):
        if not used[s]:
            rdfs(s, num_group)
            num_group += 1
    return num_group, group

# 縮約後のグラフを構築
# 入力: <N>: 頂点サイズ, <G>: 順方向の有向グラフ, <num_group>:ラベル数, <group>:各頂点のラベル番号
# 出力: G0:???, GP:縮約後のグラフの構成元頂点
def construct(N, G, label, group):
    G0 = [set() for i in range(label)]
    GP = [[] for i in range(label)]
    for v in range(N):
        lbs = group[v]
        for w in G[v]:
            lbt = group[w]
            if lbs == lbt:
                continue
            G0[lbs].add(lbt)
        GP[lbs].append(v)
    return G0, GP
    
N = int(input())
A = list(map(int,input().split()))

# 高橋くんが勝てる条件
# iを含むサイクルがある場合

graph = [[] for _ in range(N)]
rgraph = [[] for _ in range(N)]
ans = 0
for i in range(N):
    graph[i].append(A[i]-1)
    rgraph[A[i]-1].append(i)

    if i == A[i]-1:
        ans += 1

# num_group:
num_group,group = scc(N,graph,rgraph)
G0,GP = construct(N,graph,num_group,group)

for g in GP:
    if len(g) > 1:
        ans += len(g)
print(ans)
