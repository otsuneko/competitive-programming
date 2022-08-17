N,M = map(int,input().split())
graph = [[] for _ in range(N)]

for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

ans = 0
for i in range(N):
    smaller = 0
    for j in graph[i]:
        if j < i:
            smaller += 1
    if smaller == 1:
        ans += 1
print(ans)