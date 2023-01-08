# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

def dfs(s):
    seen[s] = True
    for to in graph[s]:
        if seen[to]:
            continue
        dfs(to)

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

seen = [False]*N
ans = 0
for i in range(N):
    if seen[i]:
        continue
    dfs(i)
    ans += 1

print(ans)