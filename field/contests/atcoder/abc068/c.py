from collections import deque

def bfs(dist):
    queue = deque()
    queue.append(0)
    while queue:
        s = queue.popleft()
        for to in graph[s]:
            if dist[to] != -1:
                continue
            dist[to] = dist[s] + 1
            queue.append(to)

N,M = map(int, input().split())

graph = [[] for _ in range(N)]
for i in range(M):
 a,b = map(int, input().split())
 a,b = a-1,b-1
 graph[a].append(b)
 graph[b].append(a)

dist = [-1]*N
dist[0] = 0
bfs(dist)

if 0 < dist[N-1] <= 2:
    print("POSSIBLE")
else:
    print("IMPOSSIBLE")