# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

def dfs(i,cnt):
    if i == N-1:
        print(cnt)
        exit()
    for to in graph[i]:
        dfs(to,cnt+1)

N = int(input())
P = list(map(int,input().split()))

graph = [[] for _ in range(N)]
for i in range(N-1):
    graph[P[i]-1].append(i+1)

dfs(0,0)
