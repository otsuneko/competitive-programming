import sys
import pypyjit
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
pypyjit.set_param('max_unroll_recursion=0')

import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
sys.setrecursionlimit(10**7)

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b,x,y = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append((b,x,y))
    graph[b].append((a,-x,-y))

pos = [[-1,-1] for _ in range(N)]
pos[0] = [0,0]

def dfs(s):
    if s in seen:
        return
    seen.add(s)
    for to,x,y in graph[s]:
        if to not in seen:
            pos[to] = [pos[s][0] + x, pos[s][1] + y]
            dfs(to)

seen = set()
dfs(0)

for i in range(N):
    if pos[i] == [-1,-1]:
        print("undecidable")
    else:
        print(*pos[i])