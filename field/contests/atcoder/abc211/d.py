from collections import deque
mod = 10**9+7
def bfs(dist):
    queue = deque()
    queue.append(0)
    while queue:
        v1 = queue.popleft()
        for v2 in graph[v1]:
            if dist[v2] != -1:
                if dist[v2] == dist[v1]+1:
                    count[v2] = (count[v1]+count[v2])%mod
                continue
            dist[v2] = dist[v1] + 1
            count[v2] = (count[v1]+count[v2])%mod
            queue.append(v2)

n,m = map(int, input().split())

graph = [[] for _ in range(n+1)]
for i in range(m):
 a, b = map(int, input().split())
 a,b = a-1,b-1
 graph[a].append(b)
 graph[b].append(a)

dist = [-1] * n
dist[0] = 0
count = [0]*n
count[0] = 1
bfs(dist)
print(count[n-1])


from collections import deque

def bfs(dist):
    queue = deque()
    queue.append(0)
    while queue:
        v1 = queue.popleft()
        for v2 in graph[v1]:
            if dist[v2] != -1:
                continue
            dist[v2] = dist[v1] + 1
            queue.append(v2)

N,M = map(int, input().split())

graph = [[] for _ in range(N)]
for i in range(M):
 a,b = map(int, input().split())
 a,b = a-1,b-1
 graph[a].append(b)
 graph[b].append(a)

dist = [-1]*n
dist[0] = 0
bfs(dist)
