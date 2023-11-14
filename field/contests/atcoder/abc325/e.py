import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

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

N,A,B,C = map(int,input().split())
D = [list(map(int,input().split())) for _ in range(N)]

# 入力の受け取り・隣接リストadjの構築：
adj = [[] for _ in range(2*N)]
for i,dists in enumerate(D):
    adj[i].append((i+N,0))
    for j,cost in enumerate(dists):
        adj[i].append((j, cost*A))
        adj[i+N].append((j+N,cost*B+C))

dist = [INF]*2*N
dist[0] = 0
prev = [-1]*2*N
dijkstra(dist,prev,0)
print(min(dist[N-1],dist[2*N-1]))