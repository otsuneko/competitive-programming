# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

def dfs(s):
    global ans
    ans += 1

    if ans == 10**6:
        print(ans)
        exit()

    for t in graph[s]:
        if seen[t]:
            continue
        seen[t] = True
        dfs(t)
        seen[t] = False

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

ans = 0
seen = [False]*N
seen[0] = True
dfs(0)
print(ans)