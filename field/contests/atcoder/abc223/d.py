from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport
def topological_sort(n, graph):
    # 各頂点への入次数を求める
    indeg = [0] * n
    for i in range(n):
        for to in graph[i]:
            indeg[to] += 1

    # 入次数が0の頂点はトポソ後のグラフの始点としてよい
    que = [i for i in range(n) if indeg[i] == 0]
    heapify(que)
    ret = []
    cnt = 0 # サイクル判定用
    while que:
        s = heappop(que)
        ret.append(s+1)
        for to in graph[s]:
            indeg[to] -= 1
            if indeg[to] == 0:
                heappush(que,to)
        cnt += 1

    # サイクルが存在する場合は-1
    if cnt != n:
        return [-1]
 
    return ret

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)

ans = topological_sort(N,graph)
print(*ans)