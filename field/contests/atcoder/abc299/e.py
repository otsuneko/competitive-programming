from collections import deque

def bfs(s):
    queue = deque()
    queue.append(s)
    dist = [-1]*N
    dist[s] = 0

    while queue:
        s = queue.popleft()
        for to in graph[s]:
            if dist[to] != -1:
                continue
            dist[to] = dist[s] + 1
            queue.append(to)
    return dist

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

dists = [[-1]*N for _ in range(N)]
for i in range(N):
    dists[i] = bfs(i)

# まずはすべて黒に塗って条件の通り更新
S = ["1"]*N
K = int(input())
query = []
for _ in range(K):
    p,d = map(int,input().split())
    p -= 1
    query.append((p,d))

    for i in range(N):
        if dists[p][i] < d:
            S[i] = "0"

# 条件を満たすか確認
for p,d in query:
    cnt = 0
    for i in range(N):
        if dists[p][i] == d and S[i] == "1":
            cnt += 1
    if cnt == 0:
        print("No")
        exit()
print("Yes")
print("".join(S))