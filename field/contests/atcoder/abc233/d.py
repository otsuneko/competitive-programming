# N: 処理する区間の長さ
N,K =map(int,input().split())
A = list(map(int,input().split()))

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))
# print(cumsum)
from collections import Counter
count = Counter(cumsum[1:])

ans = 0
for l in range(N):
    ans += count[K+cumsum[l]]
    count[cumsum[l+1]] -= 1

print(ans)