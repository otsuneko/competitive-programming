import sys
sys.setrecursionlimit(10**7)

def dfs(s,seen,cnt):

    if cnt == N:
        return 1

    res = 0
    for to in graph[s]:
        if seen[to] == False:
            seen[to] = True
            res += dfs(to,seen,cnt+1)
            seen[to] = False
    
    return res

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
  a,b = map(int,input().split())
  a,b = a-1,b-1
  graph[a].append(b)
  graph[b].append(a)

seen = [False]*N
seen[0] = True
ans = dfs(0,seen,1)
print(ans)