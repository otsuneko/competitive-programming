import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))
MOD = 998244353

from collections import defaultdict
dp = defaultdict(int)
dp[(0,1,INF)] = 1

for i in range(1,N):
    ndp = dp.copy()
    ndp[(i,1,INF)] += 1

    for key,val in dp.items():
        last, len, d = key
        if d == INF:
            ndp[(i,len+1,A[i]-A[last])] += val
            ndp[(i,len+1,A[i]-A[last])] %= MOD
        else:
            if A[i]-A[last] == d:
                ndp[(i,len+1,d)] += val
                ndp[(i,len+1,d)] %= MOD
    dp = ndp.copy()

ans = [0]*(N+1)
for key,val in dp.items():
    len = key[1]
    ans[len] += val
    ans[len] %= MOD

print(*ans[1:])
