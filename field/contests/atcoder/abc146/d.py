from collections import deque

def bfs(dist):
    queue = deque()
    color = 1
    for to in graph[0]:
        queue.append((to,color))
        edge[(0,to)] = color
        dist[to] = dist[0] + 1
        color += 1
    while queue:
        s,color = queue.popleft()
        cnt = 1
        for to in graph[s]:
            if dist[to] != -1:
                continue
            dist[to] = dist[s] + 1
            new_color = mod if (color+cnt)%mod == 0 else (color+cnt)%mod
            queue.append((to,new_color))
            edge[(min(s,to),max(s,to))] = new_color
            cnt += 1

N = int(input())
graph = [[] for _ in range(N)]
query = []
for _ in range(N-1):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    query.append((a,b))
    graph[a].append(b)
    graph[b].append(a)

mod = 0
for i in range(N):
    mod = max(mod,len(graph[i]))

dist = [-1]*N
dist[0] = 0
edge = dict()
bfs(dist)
print(mod)
for a,b in query:
    print(edge[(a,b)])