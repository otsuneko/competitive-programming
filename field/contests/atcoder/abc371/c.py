import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
MG = int(input())
graph_G = [[] for _ in range(N)]
for _ in range(MG):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph_G[a].append(b)
    graph_G[b].append(a)

MH = int(input())
graph_H = [[] for _ in range(N)]
for _ in range(MH):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph_H[a].append(b)
    graph_H[b].append(a)

prices = [list(map(int,input().split())) for _ in range(N-1)]

import itertools

ans = INF
for ptr in itertools.permutations(range(N)):
    su = 0
    for u in range(N):
        for v in range(u+1,N):
            a,b = ptr[u],ptr[v]
            a,b = min(a,b),max(a,b)
            if (v in graph_G[u]) != (b in graph_H[a]):
                su += prices[a][b-a-1]
    ans = min(ans,su)
print(ans)
