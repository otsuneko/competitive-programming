import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N1,N2,M = map(int,input().split())
graph = [[] for _ in range(N1)]
graph2 = [[] for _ in range(N1+N2)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    if a < N1:
        graph[a].append(b)
        graph[b].append(a)
    else:
        graph2[a].append(b)
        graph2[b].append(a)

# print(graph,graph2)

from collections import deque

def bfs(dist,graph,s):
    queue = deque()
    queue.append(s)
    while queue:
        s = queue.popleft()
        for to in graph[s]:
            if dist[to] != -1:
                continue
            dist[to] = dist[s] + 1
            queue.append(to)

dist = [-1]*N1
dist[0] = 0
bfs(dist,graph,0)
# print(dist)

dist2 = [-1]*(N1+N2)
dist2[N1+N2-1] = 0
bfs(dist2,graph2,N1+N2-1)
# print(dist2)

print(max(dist) + max(dist2)+1)
