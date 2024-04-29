import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

def dfs(s):
    vert = 1
    edge = 0
    seen.add(s)
    for to in graph[s]:
        edge += 1
        if to not in seen:
            seen.add(to)
            v,e = dfs(to)
            vert += v
            edge += e
    return vert,edge

N,M = map(int,input().split())
friends = [list(map(int,input().split())) for _ in range(M)]

graph = [[] for _ in range(N)]
for a,b in friends:
    graph[a-1].append(b-1)
    graph[b-1].append(a-1)

ans = 0
seen = set()
for i in range(N):
    if i in seen:
        continue
    v,e = dfs(i)
    ans += v*(v-1)//2 - e//2
print(ans)
