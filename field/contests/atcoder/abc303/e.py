# N = int(input())
# graph = [[] for _ in range(N)]
# G = [[] for _ in range(N)]
# for _ in range(N-1):
#     a,b = map(int,input().split())
#     a,b = a-1,b-1
#     graph[a].append(b)
#     graph[b].append(a)
#     G[a].append((b,1))
#     G[b].append((a,1))

# from collections import deque
# def tree_diameter(s):
#     dist = [None]*N
#     que = deque([s])
#     dist[s] = 0
#     while que:
#         v = que.popleft()
#         d = dist[v]
#         for w, c in G[v]:
#             if dist[w] is not None:
#                 continue
#             dist[w] = d + c
#             que.append(w)
#     d = max(dist)
#     return dist.index(d), d

# u, _ = tree_diameter(0)
# v, d = tree_diameter(u)
# パスu-vがこの木Tの直径(長さd)

N = int(input())
graph = [set() for _ in range(N)]
for _ in range(N-1):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].add(b)
    graph[b].add(a)

ans = []
for i in range(N):
    if len(graph[i]) > 2:
        ans.append(len(graph[i]))
        for to in list(graph[i]):
            if to in graph[i]:
                graph[i].remove(to)
            if i in graph[to]:
                graph[to].remove(i)

cnt = 0
for i in range(N):
    if len(graph[i]) == 2:
        cnt += 1
# print(ans,cnt)
for _ in range(cnt//2):
    ans.append(2)
print(*sorted(ans))


# cur = graph[v][0] #中心からスタート
# seen = set()
# ans = []
# flg_edge = 0 # 0ならcenter

# from collections import deque

# def bfs(s,dist):
#     queue = deque()
#     queue.append(s)
#     ans = []
#     while queue:
#         s = queue.popleft()
#         if dist[s]%3 == 0:
#             ans.append(len(graph[s]))
#         for to in graph[s]:
#             if dist[to] != -1:
#                 continue
#             dist[to] = dist[s] + 1
#             queue.append(to)
#     ans.sort()
#     print(*ans)
#     exit()

# dist = [-1]*N
# dist[cur] = 0
# bfs(cur,dist)

# cur = graph[v][0] #中心からスタート
# dist = [-1]*N
# dist[cur] = 0
# ans = []
# cnt = 1
# while 1:
#     nxt = cur

#     # 星の周り
#     if dist[cur]%3 > 0:
#         for to in graph[cur]:
#             if dist[to] == -1:
#                 dist[to] = dist[cur] + 1
#                 nxt = to
#                 cnt += 1
#     # 星の中心
#     else:
#         ans.append(len(graph[cur]))
#         for to in graph[cur]:
#             if dist[to] == -1:
#                 dist[to] = dist[cur] + 1
#                 cnt += 1
#                 if len(graph[to]) > 1:
#                     nxt = to
#     if cnt == N:
#         ans.sort()
#         print(*ans)
#         exit()
#     cur = nxt
