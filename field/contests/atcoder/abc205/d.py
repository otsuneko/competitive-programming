import bisect
import itertools
import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,Q = map(int,input().split())
A = list(map(int,input().split()))

cnt = [0]*N
cnt[0] = A[0]-1
prev = A[0]
for i in range(N-1):
    cnt[i+1] = A[i+1]-A[i]-1

cumsum = [0] + list(itertools.accumulate(cnt))

# print(cumsum)
for _ in range(Q):
    K = int(input())
    idx = bisect.bisect_left(cumsum,K)
    # print(idx)
    if idx == 1:
        print(K)
    elif idx == N+1:
        print(A[N-1]+K-cumsum[N])
    else:
        print(A[idx-2]+K-cumsum[idx-1])

