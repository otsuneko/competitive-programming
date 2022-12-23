N,M = map(int,input().split())
graph = [set() for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    if not (0<=a<N and 0<=b<N):
        print("No")
        exit()
    if a == b:
        print("No")
        exit()
    if b in graph[a]:
        print("No")
        exit()
    graph[a].add(b)
    graph[b].add(a)

print("Yes")