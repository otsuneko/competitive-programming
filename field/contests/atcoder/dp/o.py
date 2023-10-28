import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')
INF = 10**18

def dfs(l,r):
    if memo[l][r] != -INF:
        return memo[l][r]

    if l == r:
        return 0
    
    res = -INF
    res = max(res, -dfs(l+1, r) + A[l])
    res = max(res, -dfs(l,r-1) + A[r-1])

    memo[l][r] = res
    return res

N = int(input())
A = list(map(int,input().split()))
memo = [[-INF]*(N+1) for _ in range(N+1)]
print(dfs(0,N))
