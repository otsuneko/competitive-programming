from collections import defaultdict

# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)
def dfs(s,dict):

    for to in graph[s]:
        if seen[to]:
            continue
        seen[to] = True
        if dict[C[to]] == 0:
            good.append(to)
        dict[C[to]] += 1
        dfs(to,dict)
        dict[C[to]] -= 1

N = int(input())
C = list(map(int,input().split()))

graph = [[] for _ in range(N)]
for i in range(N-1):
    a,b = map(int, input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

good = [0]
seen = [False]*N
seen[0] = True
dict = defaultdict(int)
dict[C[0]] += 1
dfs(0,dict)
good.sort()
for g in good:
    print(g+1)
