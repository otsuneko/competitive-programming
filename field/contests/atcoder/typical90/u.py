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

def nCr(n, r):

    res = 1
    for i in range(r):
        res = (res*(n-i))//(i+1)

    return res

N,M =map(int,input().split())
graph = [[] for _ in range(N)]
rgraph = [[] for _ in range(N)]
for _ in range(M):
    A,B =map(int,input().split())
    A,B = A-1,B-1
    graph[A].append(B)
    rgraph[B].append(A)

label, group = scc(N,graph,rgraph)

from collections import Counter
count = Counter(group)

ans = 0
for c in count:
    ans += nCr(count[c],2)
print(ans)