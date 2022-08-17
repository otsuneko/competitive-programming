from collections import deque

def bfs(i):
    queue = deque()
    queue.append(i)
    seen[i] = True
    while queue:
        s = queue.popleft()
        for to in graph[s]:
            if seen[to]:
                if dist[to] - dist[i] > 1:
                    print("No")
                    exit()
                continue
            dist[to] = dist[s] + 1
            seen[to] = True
            queue.append(to)

N,M = map(int,input().split())

graph = [[] for _ in range(N)]
cnt = [0]*N
for _ in range(M):
    A,B = map(int,input().split())
    A,B = A-1,B-1
    graph[A].append(B)
    graph[B].append(A)
    cnt[A] += 1
    cnt[B] += 1

for c in cnt:
    if c > 2:
        print("No")
        exit()

seen = [False]*N
for i in range(N):
    dist = [-1]*N
    dist[i] = 0
    if seen[i]:
        continue
    bfs(i)

print("Yes")
