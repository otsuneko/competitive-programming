import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from collections import deque
def topological_sort(n, graph):
    # 各頂点への入次数を求める
    indeg = [0] * n
    for i in range(n):
        for to in graph[i]:
            indeg[to] += 1

    # 入次数が0の頂点はトポソ後のグラフの始点としてよい
    que = deque([i for i in range(n) if indeg[i] == 0])
    ret = []
    cnt = 0 # サイクル判定用
    while que:
        s = que.popleft()
        if s in books:
            ret.append(s+1)
        for to in graph[s]:
            indeg[to] -= 1
            if indeg[to] == 0:
                que.append(to)
        cnt += 1
    
    # サイクルが存在する場合は-1
    if cnt != n:
        return [-1]
 
    return ret

N = int(input())
graph = [[] for _ in range(N)]
out = [[] for _ in range(N)]
for i in range(N):
    _,*book = map(int,input().split())
    for b in book:
        graph[b-1].append(i)
        out[i].append(b-1)
# print(graph)

books = set()
books.add(0)
for i in range(N):
    if i not in books:
        continue
    books |= set(out[i])

ans = topological_sort(N,graph)


print(*ans[:-1])