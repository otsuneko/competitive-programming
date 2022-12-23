from collections import defaultdict
import heapq  # heapqライブラリのimport

N,M = map(int,input().split())
jobs = defaultdict(list)
for _ in range(N):
    A,B = map(int,input().split())
    jobs[A].append(B)

ans = 0
pq = []
for day in range(1,M+1):
    for job in jobs[day]:
        heapq.heappush(pq, job*-1)
    
    if pq:
        ans += heapq.heappop(pq)*-1

print(ans)