N =int(input())
A =list(map(int,input().split()))

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))

for k in range(1,N+1):
    ans = 0
    for i in range(N-k+1):
        ans = max(ans, cumsum[i+k]-cumsum[i])
    print(ans)