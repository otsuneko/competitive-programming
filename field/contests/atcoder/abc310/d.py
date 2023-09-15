import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys
sys.setrecursionlimit(10**7)

def dfs(s):
    seen.add(s)
    for to in graph[s]:
        if to not in seen:
            dfs(to)



N,T,M = map(int,input().split())
bad = set([tuple(map(int,input().split())) for _ in range(M)])

dfs(0)
