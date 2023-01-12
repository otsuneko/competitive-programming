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

# 入力の受け取り・隣接リストadjの構築：
N,M = map(int, input().split()) # ノード数, エッジ数
adj = [[] for _ in range(N)]
for _ in range(M):
    s,t,d = map(int, input().split())
    s,t = s-1,t-1
    adj[s].append((t, d))
    adj[t].append((s, d)) # 有向グラフの場合はコメントアウト

dist = [INF]*N
dist[0] = 0
prev = [-1]*N
dijkstra(dist,prev,0)

for d in dist:
    print(d)