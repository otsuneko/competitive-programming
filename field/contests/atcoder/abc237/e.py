###公式解(ダイクストラ)###
from heapq import heappush, heappop
inf=10**18
def dijkstra(d,p,s):
    ans = 0
    hq = [(0, s)] # (distance, node)
    seen = [False] * N # ノードが確定済みかどうか
    while hq:
        v = heappop(hq)[1] # ノードを pop する
        seen[v] = True
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if seen[to] == False and d[v] + cost < d[to]:
                d[to] = d[v] + cost
                ans = max(ans, H[0]-H[to]-d[to])
                heappush(hq, (d[to], to))
                p[to] = v
    return ans

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
H =list(map(int,input().split()))
adj = [[] for _ in range(N)]
for _ in range(M):
    s,t = map(int, input().split())
    s,t = s-1,t-1
    joy = H[s]-H[t]
    if H[s] > H[t]:
        adj[s].append((t, 0))
        adj[t].append((s, joy))
    else:
        adj[s].append((t, -joy))
        adj[t].append((s, 0))

dist = [inf]*N
dist[0] = 0
prev = [-1]*N
print(dijkstra(dist,prev,0))


# ###嘘解法(BFS)###
# from collections import deque

# def bfs():
#     queue = deque()
#     queue.append(0)
#     seen[0] = True
#     while queue:
#         s = queue.popleft()
#         for to in graph[s]:
#             if H[s] > H[to]:
#                 joy = H[s]-H[to]
#             else:
#                 joy = 2*(H[s]-H[to])
            
#             if seen[to] == True and joys[to] >= joys[s] + joy:
#                 continue
#             else:
#                 joys[to] = joys[s] + joy
#                 seen[to] = True
#                 queue.append(to)

# N,M = map(int, input().split())
# H =list(map(int,input().split()))

# graph = [[] for _ in range(N)]
# for i in range(M):
#  a,b = map(int, input().split())
#  a,b = a-1,b-1
#  graph[a].append(b)
#  graph[b].append(a)

# joys = [0]*N
# seen = [False]*N
# bfs()
# print(max(joys))
