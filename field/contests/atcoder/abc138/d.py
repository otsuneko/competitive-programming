# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

# 連結でないグラフの場合は、未発見の頂点が無くなるまでdfsを繰り返す
# コメントアウト箇所を有効化するとオイラーツアー可能
def dfs(s,p):

    if p != -1:
        add[s] += add[p]

    seen[s] = True
    for to in graph[s]:
        if seen[to]:
            continue
        dfs(to,s)

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
dfs(0,-1)
print(*add)