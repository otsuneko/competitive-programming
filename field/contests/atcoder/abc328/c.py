import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,Q = map(int,input().split())
S = input()

flg = [0]*N
for i in range(N-1):
    if S[i] == S[i+1]:
        flg[i] = 1

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(flg, func=operator.add))
# cumsum = list(itertools.accumulate(A[::-1], func=operator.add))[::-1] + [0] # 逆順の累積和
# print(flg)
# print(cumsum)

for _ in range(Q):
    l,r = map(int,input().split())

    ans = cumsum[r-1]-cumsum[l-1]
    print(ans)