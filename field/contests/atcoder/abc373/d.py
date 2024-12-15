import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

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
        ret.append(s)
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

    return ret # 各頂点からの最長パスが必要な場合はlongest_pathをreturnする

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
graph_w = [[] for _ in range(N)]
for _ in range(M):
    a,b,w = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph_w[a].append((b,w))

ans = [-1]*N
path = topological_sort(N,graph)
for u in path:
    if ans[u] != -1:
        continue
    for v,w in graph_w[u]:
        ans[u] = ans[v] - w

print(*ans)
