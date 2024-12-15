from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right

N = int(input())
A = list(map(int,input().split()))
A.sort()

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))
print(cumsum)

mod = 10**8
ans = 0
for i,a in enumerate(A):
    idx = bisect_left(A,mod-a)
    print(A,idx)
    ans += max(0,cumsum[idx]-cumsum[i] + a * (idx-i))
    print(ans)
    ans += (cumsum[N]-cumsum[idx] + a * (N-idx)) % mod
    print(ans)
print(ans)
