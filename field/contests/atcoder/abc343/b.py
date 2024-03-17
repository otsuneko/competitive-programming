import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N =  int(input())
A =  [list(map(int,input().split())) for _ in range(N)]
adj = [[] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if A[i][j] == 1:
            adj[i].append(j+1)

cnt = 0
for i in range(N):
    if len(adj[i]):
        print(*adj[i])
    cnt += len(adj[i])

if cnt == 0:
    print()
