N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

ans = 0
for i in range(N):
    for j in range(i+1,N):
        for k in range(j+1,N):
            if j in graph[i] and k in graph[j] and i in graph[k]:
                ans += 1
print(ans)