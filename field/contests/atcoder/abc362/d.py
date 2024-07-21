import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from heapq import heappush, heappop
INF=10**18
def dijkstra(d,s):
    hq = [(A[0], s)] # (distance, node)
    while hq:
        cost,v = heappop(hq) # ノードを pop する
        if dist[v] < cost:
            continue
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if d[v] + cost + A[to] < d[to]:
                d[to] = d[v] + cost + A[to]
                heappush(hq, (d[to], to))
    return dist


# 入力の受け取り・隣接リストadjの構築：
N,M = map(int, input().split()) # ノード数, エッジ数
A = list(map(int,input().split()))
adj = [[] for _ in range(N)]
for _ in range(M):
    s,t,d = map(int, input().split())
    s,t = s-1,t-1
    adj[s].append((t, d))
    adj[t].append((s, d))

dist = [INF]*N
dist[0] = A[0]
dijkstra(dist,0)
print(*dist[1:])
