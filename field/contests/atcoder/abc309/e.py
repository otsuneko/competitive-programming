import sys
input = lambda: sys.stdin.readline().rstrip()
sys.setrecursionlimit(10**7)
INF = 10**18

def dfs(x):
    y = ma[x]
    for to in graph[x]:
        ma[to] = max(ma[to], y-1)
        dfs(to)

N,M = map(int,input().split())
P = list(map(int,input().split()))

graph = [[] for _ in range(N)]
for i in range(N-1):
    parent = P[i]-1
    graph[parent].append(i+1)

ma = [-1]*N
for _ in range(M):
    x,y = map(int,input().split())
    x -= 1
    ma[x] = max(ma[x],y)

dfs(0)
ans = 0
for i in range(N):
    if ma[i] >= 0:
        ans += 1
print(ans)
