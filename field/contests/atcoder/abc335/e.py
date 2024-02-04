import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from heapq import heappush, heappop
def dijkstra(d,seen,ans,s):
    hq = [(0, seen, ans, s)] # (distance, node)
    while hq:
        cost,seen,ans,v = heappop(hq) # ノードを pop する
        if v == N-1:
            print(len(ans))
            exit()

        if dist[v] < cost:
            continue
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if cost != INF and d[v] * cost < d[to] and to not in seen:
                d[to] = d[v] * cost
                seen.add(to)
                ans.add(A[to])

                heappush(hq, (d[to], seen,ans,to))
    return dist

N,M = map(int,input().split())
A = list(map(int,input().split()))

adj = [[] for _ in range(N)]
for _ in range(M):
    s,t = map(int, input().split())
    s,t = s-1,t-1
    if A[s] > A[t]:
        d1 = INF
        d2 = 1/A[t]
    else:
        d1 = 1/A[s]
        d2 = INF

    adj[s].append((t, d1))
    adj[t].append((s, d2))

dist = [INF]*N
dist[0] = 0
dijkstra(dist,set([0]),set([A[0]]),0)
