import heapq  # heapqライブラリのimport
N,M = map(int,input().split())
G = [[] for _ in range(N)]
deg = [0]*N
for _ in range(M):
    A,B = map(int,input().split())
    A,B = A-1,B-1
    G[A].append(B)
    deg[B] += 1

hq = [v for v in range(N) if deg[v]==0]
heapq.heapify(hq)
ans = []
cnt = 0
while hq:
    v = heapq.heappop(hq)
    ans.append(v+1)
    for t in G[v]:
        deg[t] -= 1
        if deg[t]==0:
            heapq.heappush(hq,t)
    cnt += 1

if cnt != N:
    print(-1)
else:
    print(*ans)