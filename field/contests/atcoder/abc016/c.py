# from heapq import heappush, heappop
# INF=10**18
# def dijkstra(d,p,s):
#     hq = [(0, s)] # (distance, node)
#     while hq:
#         cost,v = heappop(hq) # ノードを pop する
#         if dist[v] < cost:
#             continue
#         for to, cost in adj[v]: # ノード v に隣接しているノードに対して
#             if d[v] + cost < d[to]:
#                 d[to] = d[v] + cost
#                 heappush(hq, (d[to], to))
#                 p[to] = v
#     return dist

# #s→tの最短経路復元
# def get_path(t):
#     if dist[t] == INF:
#         return []
#     path = []
#     while t != -1:
#         path.append(t)
#         t = prev[t]
#     #t->sの順になっているので逆順にする
#     path.reverse()
#     return path

# N,M = map(int,input().split())
# adj = [[] for _ in range(N)]
# for _ in range(M):
#     a,b = map(int,input().split())
#     a,b = a-1,b-1
#     adj[a].append((b,1))
#     adj[b].append((a,1))

# for i in range(N):
#     dist = [INF]*N
#     dist[i] = 0
#     prev = [-1]*N
#     dijkstra(dist,prev,i)
#     ans = 0
#     for d in dist:
#         if d == 2:
#             ans += 1
#     print(ans)


N,M = map(int,input().split())
friends = [set() for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    friends[a].add(b)
    friends[b].add(a)

ans = [set() for _ in range(N)]
for i in range(N):
    for j in range(i+1,N):
        if len(friends[i] & friends[j]):
            if j not in friends[i]:
                ans[i].add(j)
            if i not in friends[j]:
                ans[j].add(i)

for a in ans:
    print(len(a))