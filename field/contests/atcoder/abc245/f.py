import sys
sys.setrecursionlimit(10**7)

# 強連結成分分解(SCC): グラフGに対するSCCを行う
# 入力: <N>: 頂点サイズ, <G>: 順方向の有向グラフ, <RG>: 逆方向の有向グラフ
# 出力: (<ラベル数>, <各頂点のラベル番号>)
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

N,M =map(int,input().split())
G = [[] for _ in range(N)]
RG = [[] for _ in range(N)]
for _ in range(M):
    u,v =map(int,input().split())
    u,v = u-1, v-1
    G[u].append(v)
    RG[v].append(u)

num_group, group = scc(N,G,RG)
print(num_group, group)
G0,GP = construct(N,G,num_group,group)
print(G0,GP)

ans = 0
for i,g in enumerate(G0):
    if len(g):
        ans += len(GP[i])
print(ans)