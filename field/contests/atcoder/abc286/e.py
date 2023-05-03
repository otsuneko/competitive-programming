N = int(input())
A = list(map(int,input().split()))
S = [list(input()) for _ in range(N)]
Q = int(input())
graph = [[] for _ in range(N)]
for _ in range(Q):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)