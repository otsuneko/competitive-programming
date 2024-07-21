import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
from collections import defaultdict

def isok(s):
    if len(s) == K and s == s[::-1]:
        return False
    return True

N,K = map(int, input().split())
S = input()
MOD = 998244353

dp = defaultdict(int)

dp[""] = 1

for i in range(N):
    ndp = defaultdict(int)
    for key,val in dp.items():
        for c in "AB":
            if S[i] in [c, "?"]:
                s = key+c
                if isok(s[-K:]):
                    ndp[s[-K:]] += val
                    ndp[s[-K:]] %= MOD
    dp = ndp

print(sum(dp.values())%MOD)
