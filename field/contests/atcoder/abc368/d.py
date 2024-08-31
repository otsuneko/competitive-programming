import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
graph = [set() for _ in range(N)]
for _ in range(N-1):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].add(b)
    graph[b].add(a)
V = set(list(map(lambda x: int(x)-1,input().split())))
degrees = [len(graph[i]) for i in range(N)]

deg_one = [i for i,deg in enumerate(degrees) if deg == 1 and i not in V]

ans = N
for v in deg_one:
    if v in V:
        continue
    ans -= 1
    u = graph[v].pop()
    graph[u].remove(v)
    if len(graph[u]) == 1:
        deg_one.append(u)

print(ans)
