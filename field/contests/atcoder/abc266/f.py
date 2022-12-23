import sys
sys.setrecursionlimit(10**7)
from collections import deque
import copy

def bfs(s):
    queue = deque()
    queue.append(([s,[s],set([s])]))
    while queue:
        cur,path,seen = queue.popleft()
        for to in graph[cur]:
            if to in seen:
                if to != path[-2]:
                    path.append(to)
                    # print(cur,to,path,seen)
                    for i in range(len(path)):
                        if path[i] == path[-1]:
                                return path[i+1:]
                else:
                    continue
            path2 = path[:]
            path2.append(to)
            seen2 = copy.copy(seen)
            seen2.add(to)
            queue.append((to,path2,seen2))

def dfs(cur,pre,li):
    li.append(cur)
    if cur in cycle:
        return li
    
    for to in graph[cur]:
        if to != pre:
            li = dfs(to,cur,li)

    return li

N = int(input())
graph = [[] for _ in range(N+1)]
graph2 = [set() for _ in range(N+1)]
for _ in range(N):
    a,b = map(int,input().split())
    graph[a].append(b)
    graph[b].append(a)
    graph2[a].add(b)
    graph2[b].add(a)

cycle = []
for i in range(1,N+1):
    if len(graph[i]) == 1:
        cycle = bfs(i)
        break

# print(cycle)

category = [i for i in range(N+1)]
for i in range(1,N+1):
    # 葉ノードから閉路要素にぶつかるまで探索
    if len(graph[i]) == 1:
        nodes = dfs(i,-1,[])
        for n in nodes:
            category[n] = nodes[-1]

# print(category)

Q = int(input())
for _ in range(Q):
    x,y = map(int,input().split())
    if category[x] == category[y]:
        print("Yes")
    else:
        print("No")