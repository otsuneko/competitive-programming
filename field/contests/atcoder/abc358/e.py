import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

MOD = 998244353

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

memo = dict()
def dfs(n,li):
    res = 0

    if n == K:
        return 0

    t = tuple(li)
    if (n,t) in memo:
        return memo[(n,t)]

    for i in range(26):
        if li[i] == 0:
            continue

        # 使う
        li[i] -= 1
        res = (res + dfs(n+1,li)) % MOD
        li[i] += 1

    memo[(n,t)] = res+1

    return res+1

K = int(input())
C = list(map(int, input().split()))
print(dfs(0, C))
