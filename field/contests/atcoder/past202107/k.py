from heapq import heappush, heappop
inf=10**18
def dijkstra(d,p,s):
    hq = [(0, s)] # (distance, node)
    seen = [False] * N # ノードが確定済みかどうか
    while hq:
        v = heappop(hq)[1] # ノードを pop する
        seen[v] = True
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if seen[to] == False and d[v] + cost <= d[to]:
                d[to] = d[v] + cost
                heappush(hq, (d[to], to))
                p[to] = v
    return dist

#s→tの最短経路復元
def get_path(t):
    if dist[t] == inf:
        return []
    path = []
    while t != -1:
        path.append(t)
        t = prev[t]
    #t->sの順になっているので逆順にする
    path.reverse()
    return path

import sys
sys.setrecursionlimit(10**7)
def dfs(s,time,satisfy):
    global visited
    global ans

    if s == N-1:
        ans = max(ans, satisfy)
        return 

    for to, cost in adj[s]:
        if time + cost <= min_cost:
            dfs(to,time+cost, satisfy + A[to])

# 入力の受け取り・隣接リストadjの構築：
N,M = map(int, input().split()) # ノード数, エッジ数
A = list(map(int,input().split()))

adj = [[] for _ in range(N)]
for _ in range(M):
    u,v,t = map(int, input().split())
    u,v = u-1,v-1
    adj[u].append((v, t))

dist = [inf]*N
dist[0] = 0
prev = [-1]*N
dijkstra(dist,prev,0)

min_cost = dist[N-1]

ans = 0
visited = [False]*N
visited[0] = True
dfs(0,0,A[0])
print(ans)