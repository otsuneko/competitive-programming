from heapq import heappush, heappop
INF=10**18
def dijkstra(d,p,s):
    hq = [(0, s)] # (distance, node)
    while hq:
        cost,v = heappop(hq) # ノードを pop する
        if dist[v] < cost:
            continue
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if d[v] + cost < d[to]:
                d[to] = d[v] + cost
                heappush(hq, (d[to], to))
                p[to] = v
    return dist

#s→tの最短経路復元
def get_path(t):
    if dist[t] == INF:
        return []
    path = []
    while t != -1:
        path.append(t)
        t = prev[t]
    #t->sの順になっているので逆順にする
    path.reverse()
    return path

H,W = map(int,input().split())
C = [list(map(int,input().split())) for _ in range(10)]
A = [list(map(int,input().split())) for _ in range(H)]


adj = [[] for _ in range(10)]
for i in range(10):
    for j in range(10):
        c = C[i][j]
        adj[i].append((j, c))

mi = [10**18]*10
for i in range(10):
    dist = [INF]*10
    dist[i] = 0
    prev = [-1]*10
    dijkstra(dist,prev,i)
    mi[i] = dist[1]

ans = 0
for i in range(H):
    for j in range(W):
        if A[i][j] != -1:
            ans += mi[A[i][j]]
print(ans)