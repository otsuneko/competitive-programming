import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
MOD = 998244353

N = int(input())
A = list(map(int,input().split()))

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))

cnt_len = [[0]*12 for _ in range(N)]

for i in range(N-1,-1,-1):
    for dig in range(11):
        if i < N-1:
            cnt_len[i][dig+1] = cnt_len[i+1][dig+1]
    l = len(str(A[i]))
    cnt_len[i][l] += 1

ans = 0
for i in range(N-1):
    ans = (ans + cumsum[-1] - cumsum[i+1])%MOD

    for dig in range(11):
        ans = (ans + A[i] * 10**dig * (cnt_len[i+1][dig]))%MOD

print(ans%MOD)
