N,Q = map(int,input().split())
A = [0] + list(map(int,input().split()))
A2 = []
for i in range(N):
    A2.append(A[i+1]-A[i]-1)

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A2, func=operator.add))

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
# print(cumsum)
for _ in range(Q):
    K = int(input())
    idx = bisect_left(cumsum,K)-1
    base = A[idx]
    print(base + K - cumsum[idx])