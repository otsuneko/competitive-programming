from heapq import heappush, heappop
inf=10**18
def dijkstra(d,p,s):
    hq = [(0, s)] # (distance, node)
    seen = [False] * N # ノードが確定済みかどうか
    while hq:
        v = heappop(hq)[1] # ノードを pop する
        seen[v] = True
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if seen[to] == False and d[v] + cost < d[to]:
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

# 入力の受け取り・隣接リストadjの構築：
N,M = map(int, input().split()) # ノード数, エッジ数
adj = [[] for _ in range(N)]
for _ in range(M):
    s,t,d = map(int, input().split())
    s,t = s-1,t-1
    adj[s].append((t,d))
    adj[t].append((s,d))

dist = [inf]*N
dist[0] = 0
prev = [-1]*N
dijkstra(dist,prev,0)

dist2 = [inf]*N
dist2[N-1] = 0
prev2 = [-1]*N
dijkstra(dist2,prev2,N-1)

for k in range(N):
    print(dist[k] + dist2[k])