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
        cnt += 1

    # サイクルが存在する場合は空リスト
    if cnt != n:
        return []
 
    return ret

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)

ans = topological_sort(N,graph,True)
if ans:
    print(*ans)
else:
    print(-1)