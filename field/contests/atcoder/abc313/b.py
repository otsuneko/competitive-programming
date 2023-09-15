import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)

from collections import deque
def topological_sort(n, graph):
    # 各頂点への入次数を求める
    indeg = [0] * n
    for i in range(n):
        for to in graph[i]:
            indeg[to] += 1

    indeg_ori = indeg[:]
    que = deque([i for i in range(n) if indeg[i] == 0])
    ret = []
    while que:
        s = que.popleft()
        ret.append(s)
        for to in graph[s]:
            indeg[to] -= 1
            if indeg[to] == 0:
                que.append(to)
    
    cnt = 0
    for s in ret:
        if indeg_ori[s] == 0:
            cnt += 1
        else:
            break
    
    if cnt == 1:
        print(ret[0]+1)
    else:
        print(-1)
    

topological_sort(N,graph)