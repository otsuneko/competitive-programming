from heapq import heappush, heappop
inf=10**18
def dijkstra(d,p,s):
    hq = [(0, s)] # (distance, node)
    seen = [False] * N # ノードが確定済みかどうか

    while hq:
        v = heappop(hq)[1] # ノードを pop する
        if seen[v] == True:
            continue
        seen[v] = True
        if v == Y:
            return d

        for to, cost, cycle in adj[v]: # ノード v に隣接しているノードに対して
            if seen[to] == True:
                continue
            wait = (d[v]+cycle-1)//cycle * cycle
            if wait + cost < d[to]:
                d[to] = wait + cost
                heappush(hq, (d[to], to))
                p[to] = v
    return d

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
N,M,X,Y = map(int, input().split()) # ノード数, エッジ数
X,Y = X-1,Y-1
adj = [[] for _ in range(N)]
for _ in range(M):
    a,b,t,k = map(int, input().split())
    a,b = a-1,b-1
    adj[a].append((b, t, k))
    adj[b].append((a, t, k))

dist = [inf]*N
dist[X] = 0
prev = [-1]*N
dijkstra(dist,prev,X)

if dist[Y] == inf:
    print(-1)
else:
    print(dist[Y])
