N = int(input())

graph = [[] for _ in range(N)]
for i in range(N-1):
 a,b = map(int, input().split())
 a,b = a-1,b-1
 graph[a].append(b)
 graph[b].append(a)

for i in range(N):
    if len(graph[i]) == N-1:
        print("Yes")
        exit()
print("No")