# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

# コメントアウト箇所を有効化するとオイラーツアー可能
def dfs(s):
    global cnt

    # 行きがけ
    cnt += add[s]
    ans[s] = cnt
    # euler.append(s+1)

    seen[s] = True
    for to in graph[s]:
        if seen[to]:
            continue
        dfs(to)
        # euler.append(s+1)

    cnt -= add[s]

N,Q =map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(N-1):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

add = [0]*N
for _ in range(Q):
    p,x =map(int,input().split())
    p -= 1
    add[p] += x

seen = [False]*N
ans = [-1]*N
cnt = 0
dfs(0)
print(*ans)