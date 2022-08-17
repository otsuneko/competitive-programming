from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
N,Q = map(int,input().split())
A = list(map(int,input().split()))
X = [int(input()) for _ in range(Q)]
A.sort()

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))

s = sum(A)
for x in X:
    idx = bisect(A,x)
    ans = (cumsum[N] - cumsum[idx]) - (cumsum[idx]) + idx*x - (N-idx)*x
    print(ans)