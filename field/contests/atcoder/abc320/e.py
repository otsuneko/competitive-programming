import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport

N,M = map(int,input().split())
somen = []

hq1 = list(range(N))
heapify(hq1)
hq2 = []
ans = [0]*N
for _ in range(M):
    t,w,s = map(int,input().split())

    while hq2 and hq2[0][0] <= t:
        t2,idx = heappop(hq2)
        heappush(hq1,idx)

    if hq1:
        idx = heappop(hq1)
        heappush(hq2,(t+s,idx))
        ans[idx] += w

for a in ans:
    print(a)