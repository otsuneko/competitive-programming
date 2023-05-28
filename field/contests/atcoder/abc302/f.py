N,M = map(int,input().split())
graph = [[] for _ in range(M+1+N)]
for i in range(N):
    A = int(input())
    S = set(map(int,input().split()))
    for s in S:
        graph[s].append(i+M+1)
        graph[i+M+1].append(s)

from collections import deque

def bfs(dist):
    queue = deque()
    queue.append(1)
    while queue:
        s = queue.popleft()
        if s == M:
            print((dist[M]-1)//2)
            exit()
        for to in graph[s]:
            if dist[to] != -1:
                continue
            dist[to] = dist[s] + 1
            queue.append(to)

dist = [-1]*(M+1+N)
dist[1] = 0
bfs(dist)
print(-1)