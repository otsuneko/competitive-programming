# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

# 連結でないグラフの場合は、未発見の頂点が無くなるまで始点を変えてdfsを繰り返す
def dfs(s):
    global cnt

    # 行きがけ
    cnt += 1
    timestamp[s][0] = cnt
    euler.append(s+1)

    seen[s] = True
    for to in graph[s]:
        if seen[to]:
            continue
        dfs(to)
        euler.append(s+1)

    # 帰りがけ
    cnt += 1
    timestamp[s][1] = cnt

N = int(input())
graph = [[] for _ in range(N)]
for _ in range(N-1):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

for i in range(N):
    graph[i].sort()

timestamp = [[0,0] for _ in range(N)]
seen = [False]*N
cnt = 0
euler = []
dfs(0)
print(*euler)