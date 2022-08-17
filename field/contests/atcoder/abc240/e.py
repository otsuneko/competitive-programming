# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

def dfs(s):
    global num

    seen[s] = True
    mi = 10**18
    ma = 0
    cnt = 0
    for to in graph[s]:
        if seen[to] == True:
            continue
        tmi,tma = dfs(to)
        mi = min(mi,tmi)
        ma = max(ma,tma)
        cnt += 1

    if cnt == 0:
        ans[s] = [num,num]
        mi = ma = num
        num += 1
    else:
        ans[s] = [mi,ma]

    return mi,ma

N = int(input())
graph = [[] for _ in range(N)]
for _ in range(N-1):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

ans = [[0,0] for _ in range(N)]
num = 1
seen = [False]*N
dfs(0)

for a in ans:
    print(*a)