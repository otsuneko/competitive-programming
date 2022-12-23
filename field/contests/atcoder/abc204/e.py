from heapq import heappush, heappop
inf=10**18
def dijkstra(d,p,s):
    hq = [(0, s)] # (distance, node)
    seen = [False] * N # ノードが確定済みかどうか
    now = 0

    while hq:
        v = heappop(hq)[1] # ノードを pop する
        seen[v] = True
        for to, cost1, cost2 in adj[v]: # ノード v に隣接しているノードに対して
            tmp_wait = int(cost2**0.5)
            min_cost = inf
            wait = tmp_wait
            for i in range(max(0,tmp_wait-10),tmp_wait+10):
                cost = cost1 + cost2//(now+i+1)
                # print(cost)
                if cost < min_cost:
                    min_cost = cost
                    wait = i
                else:
                    break
            if seen[to] == False and d[v] + cost + min_cost < d[to]:
                now += wait
                d[to] = d[v] + cost + min_cost
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

N,M = map(int,input().split())
adj = [[] for _ in range(N)]
for _ in range(M):
    A,B,C,D = map(int,input().split())
    A,B = A-1,B-1
    adj[A].append([B,C,D])
    adj[B].append([A,C,D])

dist = [inf]*N
dist[0] = 0
prev = [-1]*N
dijkstra(dist,prev,0)

if dist[N-1] == 10**18:
    print(-1)
else:
    print(dist[N-1])