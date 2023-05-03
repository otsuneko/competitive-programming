N,M = map(int, input().split())

graph = [[] for _ in range(N)]
check = set()
M2 = 0
for i in range(M):
    a,b = map(int, input().split())
    a,b = a-1,b-1
    if (min(a,b),max(a,b)) not in check:
        graph[a].append(b)
        graph[b].append(a)
        check.add((min(a,b),max(a,b)))
        M2 += 1

if N != M2+1:
    print("No")
    exit()

cnt_one = 0
cnt_two = 0
for i in range(N):
    if len(graph[i]) == 1:
        cnt_one += 1
    elif len(graph[i]) == 2:
        cnt_two += 1
    else:
        print("No")
        exit()

if not (cnt_one == 2 and cnt_two == N-2):
    print("No")
    exit()


# N: 木Tの頂点数
# G[u] = [(w, c), ...]:
#   頂点uに隣接する頂点wとそれを繋ぐ辺の長さc
from collections import deque
def tree_diameter(s):
    dist = [-1]*N
    que = deque([s])
    dist[s] = 0
    while que:
        v = que.popleft()
        d = dist[v]
        for w in graph[v]:
            if dist[w] != -1:
                continue
            dist[w] = d + 1
            que.append(w)
    d = max(dist)
    return dist.index(d), d

u, _ = tree_diameter(0)
v, d = tree_diameter(u)
# パスu-vがこの木Tの直径(長さd)

if d == N-1:
    print("Yes")
else:
    print("No")