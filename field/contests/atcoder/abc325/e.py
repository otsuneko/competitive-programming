import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from heapq import heappush, heappop
def dijkstra(d,s):
    hq = [(0, s)] # (distance, node)
    while hq:
        cost,v = heappop(hq) # ノードを pop する
        if d[v] < cost:
            continue
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if d[v] + cost < d[to]:
                d[to] = d[v] + cost
                heappush(hq, (d[to], to))

    return dist

N,A,B,C = map(int,input().split())
adj = [[] for _ in range(2*N)]
for i in range(N):
    tmp = list(map(int,input().split()))
    for j in range(N):
        adj[i].append((j,tmp[j]*A)) # car->car
        adj[i].append((j+N,tmp[j]*B+C)) # car->train
        adj[i+N].append((j+N,tmp[j]*B+C)) # train->train

dist = [INF]*2*N
dist[0] = 0
dijkstra(dist,0)

# print(dist)
print(min(dist[N-1],dist[2*N-1]))