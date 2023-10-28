from heapq import heapify, heappush, heappop  # heapqライブラリのimport
from collections import deque
def topological_sort(n, graph, isLexicograph=False):
    # 各頂点への入次数を求める
    indeg = [0]*n
    for s in range(n):
        for to in graph[s]:
            indeg[to] += 1

    # 入次数が0の頂点はトポソ後のグラフの始点としてよい
    queue = [i for i in range(n) if indeg[i] == 0]
    if isLexicograph:
        heapify(queue)
    else:
        queue = deque(queue)
    ret = []
    cnt = 0 # サイクル判定用
    longest_path = [0]*N # 有向グラフにおける各頂点からの最長パス
    while queue:
        s = heappop(queue) if isLexicograph else queue.popleft()
        ret.append(s+1)
        for to in graph[s]:
            indeg[to] -= 1
            if indeg[to] == 0:
                if isLexicograph:
                    heappush(queue,to)
                else:
                    queue.append(to)
                longest_path[to] = max(longest_path[to], longest_path[s]+1)
        cnt += 1

    # サイクルが存在する場合は空リストを返す
    if cnt != n:
        return []
 
    return ret,longest_path # 各頂点からの最長パスが必要な場合はlongest_pathをreturnする

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)

_,ans = topological_sort(N,graph)
print(max(ans))

# import sys,pypyjit
# sys.setrecursionlimit(10**7)
# pypyjit.set_param('max_unroll_recursion=0')

# def dfs(s):
#     if memo[s] != -1:
#         return memo[s]

#     res = 0
#     for to in graph[s]:
#         res = max(res, dfs(to) + 1)
    
#     memo[s] = res
#     return res

# N,M = map(int,input().split())
# graph = [[] for _ in range(N)]
# for _ in range(M):
#     a,b = map(int,input().split())
#     a,b = a-1,b-1
#     graph[a].append(b)

# memo = [-1]*N
# ans = 0
# for s in range(N):
#     ans = max(ans, dfs(s))
# print(ans)