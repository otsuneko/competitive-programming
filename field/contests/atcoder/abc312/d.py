import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

li = []
for s in S:
    if s == "(":
        li.append(1)
    elif s == ")":
        li.append(-1)
    else:
        li.append(0)

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(li, func=operator.add))
# cumsum = list(itertools.accumulate(A[::-1], func=operator.add))[::-1] + [0] # 逆順の累積和

dp = [0]*(len(S)+1)
MOD = 998244353

