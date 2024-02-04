import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
# Pythonで提出!!

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

# 連結でないグラフの場合は、未発見の頂点が無くなるまでdfsを繰り返す必要あり
# コメントアウト箇所を有効化するとオイラーツアー可能
def dfs(s):
    global cnt

    # 行きがけ
    cnt += 1

    seen[s] = True
    for to in graph[s]:
        if seen[to]:
            continue
        dfs(to)
        if s == 0:
            if len(ans) == 0:
                ans.append(cnt-1)
                cumsum.append(cnt-1)
            else:
                diff = cnt-cumsum[-1]-1
                ans.append(diff)
                cumsum.append(cumsum[-1] + diff)


N = int(input())
graph = [[] for _ in range(N)]
for _ in range(N-1):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

for i in range(N):
    graph[i].sort()

stamp = [[0,0] for _ in range(N)]
seen = [False]*N
cnt = 0
ans = []
cumsum = [0]
if len(graph[0]) == 1:
    print(1)
    exit()

dfs(0)
ans.sort()
# print(ans)
# print(cumsum)
print(sum(ans[:-1])+1)