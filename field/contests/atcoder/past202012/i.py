# 解法1
# N,M,K = map(int,input().split())
# H = list(map(int,input().split()))
# C = set(list(map(int,input().split())))
# adj = [[] for _ in range(N)]

# ans = [-1]*N
# village = []
# for i in range(N):
#     if i+1 in C:
#         ans[i] = 0
#     village.append([i,H[i]])

# from operator import itemgetter
# village.sort(key=itemgetter(1))

# for _ in range(M):
#     a,b = map(int,input().split())
#     a,b = a-1,b-1
#     if H[a] > H[b]:
#         adj[a].append(b)
#     else:
#         adj[b].append(a)

# for v in village:
#     if ans[v[0]] != -1:
#         continue
#     for to in adj[v[0]]:
#         if ans[to] != -1:
#             ans[v[0]] = min(ans[v[0]], ans[to] + 1) if ans[v[0]] != -1 else ans[to]+1
            
# for a in ans:
#     print(a)

# 解法2
from collections import deque

def bfs(dist):
    queue = deque()
    used = [False]*N

    for c in C:
        queue.append(c-1)
        dist[c-1] = 0
        used[c-1] = True
    while queue:
        s = queue.popleft()
        for t in graph[s]:
            if dist[t] != -1 or used[t] == True:
                continue
            dist[t] = dist[s] + 1
            queue.append(t)
            used[t] = True

N,M,K = map(int,input().split())
H = list(map(int,input().split()))
C = set(list(map(int,input().split())))
graph = [[] for _ in range(N)]
ans = [-1]*N

for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    if H[a] < H[b]:
        graph[a].append(b)
    else:
        graph[b].append(a)

bfs(ans)

for a in ans:
    print(a)