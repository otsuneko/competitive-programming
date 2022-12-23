from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport

N,L = map(int,input().split())
A = list(map(int,input().split()))
if sum(A) < L:
    A.append(L - sum(A))
    N += 1

heapify(A)

ans = 0
for _ in range(N-1):
    mi = heappop(A)
    mi2 = heappop(A)
    ans += mi+mi2
    heappush(A,mi+mi2)

print(ans)