# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

memo = {}
memo[0] = 1
def dfs(n):
    if n == 0:
        return 1
    elif n in memo:
        return memo[n]
    memo[n] = dfs(n//2) + dfs(n//3)
    return memo[n]

N = int(input())
print(dfs(N))