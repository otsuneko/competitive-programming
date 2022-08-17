from collections import deque

def bfs(dist):
    queue = deque()
    queue.append(K-1)
    while queue:
        s = queue.popleft()
        for to,cost in graph[s]:
            if dist[to] != -1:
                continue
            dist[to] = dist[s] + cost
            queue.append(to)

N = int(input())
graph = [[] for _ in range(N)]
for _ in range(N-1):
    a,b,c = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append((b,c))
    graph[b].append((a,c))

Q,K = map(int,input().split())
dist = [-1]*N
dist[K-1] = 0
bfs(dist)

for _ in range(Q):
    x,y = map(int,input().split())
    x,y = x-1,y-1
    print(dist[x]+dist[y])