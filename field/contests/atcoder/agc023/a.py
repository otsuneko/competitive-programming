N = int(input())
A = list(map(int,input().split()))

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))

ans = 0
from collections import defaultdict
dict = defaultdict(int)
for c in cumsum:
    if dict[c]:
        ans += dict[c]
    dict[c] += 1
print(ans)