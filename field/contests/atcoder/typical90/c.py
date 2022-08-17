# N: 木Tの頂点数
# G[u] = [(w, c), ...]:
# 頂点uに隣接する頂点wとそれを繋ぐ辺の長さc
from collections import deque
def tree_diameter(s):
    dist = [None]*N
    que = deque([s])
    dist[s] = 0
    while que:
        v = que.popleft()
        d = dist[v]
        for w, c in G[v]:
            if dist[w] is not None:
                continue
            dist[w] = d + c
            que.append(w)
    d = max(dist)
    return dist.index(d), d

N = int(input())
G = [[] for _ in range(N)]
for i in range(N-1):
    s, t = map(int, input().split())
    s, t = s-1,t-1
    G[s].append((t,1))
    G[t].append((s,1))

u, _ = tree_diameter(0)
v, d = tree_diameter(u)
print(d+1)


### Dijkstraで木の直径(AC) ###
# from heapq import heappush, heappop
# inf=float("inf")
# def dijkstra(d,p,s,n):
#     hq = [(0, s)] # (distance, node)
#     seen = [False] * n # ノードが確定済みかどうか
#     while hq:
#         v = heappop(hq)[1] # ノードを pop する
#         seen[v] = True
#         for to, cost in adj[v]: # ノード v に隣接しているノードに対して
#             if seen[to] == False and d[v] + cost < d[to]:
#                 d[to] = d[v] + cost
#                 heappush(hq, (d[to], to))
#                 p[to] = v
#     return dist

# #r→tの最短経路復元
# def get_path(t):
#     if dist[t] == inf:
#         return []
#     path = []
#     while t != -1:
#         path.append(t)
#         t = prev[t]
#     #t->sの順になっているので逆順にする
#     path.reverse()
#     return path

# N = int(input())

# # 入力の受け取り・隣接リストadjの構築：
# adj = [[] for _ in range(N)]
# for i in range(N-1):
#     s, t = map(int, input().split())
#     s, t = s-1,t-1
#     adj[s].append((t, 1))
#     adj[t].append((s, 1))


# dist = [inf]*N
# dist[0] = 0
# prev = [-1]*N
# dijkstra(dist,prev,0,N)

# idx = 0
# max_dist = 0
# for i in range(N):
#     if dist[i] > max_dist:
#         max_dist = dist[i]
#         idx = i

# dist = [inf]*N
# dist[idx] = 0
# prev = [-1]*N
# dijkstra(dist,prev,idx,N)

# max_dist = 0
# for i in range(N):
#     if dist[i] > max_dist:
#         max_dist = dist[i]

# print(max_dist+1)


### original (WA) ###
# ans = 0
# for i in range(N):
#     dist = [inf]*N
#     dist[i] = 0
#     prev = [-1]*N
#     dijkstra(dist,prev,i,N)

#     path_list = []
#     for j in range(N):
#         p = get_path(j)
#         path_list.append(p[1:])
#         print(p[1:])
#     for j in range(len(path_list)):
#         for k in range(j+1,len(path_list)):
#             if set(path_list[j]) & set(path_list[k]) == set():
#                 ans = max(ans,len(path_list[j])+len(path_list[k])+1)
# print(ans)