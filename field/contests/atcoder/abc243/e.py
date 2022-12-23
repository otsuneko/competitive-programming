N,M =map(int,input().split())
graph = [[] for _ in range(M)]
for _ in range(M):
    a,b,c =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append((b,c))
    graph[b].append((a,c))

