import sys
sys.setrecursionlimit(10**7)
def dfs(n):
    if n == N:
        return 1
    if seen[n]:
        return seen[n]

    if n+L <= N:
        seen[n] = (seen[n]+dfs(n+L)+dfs(n+1))%(10**9+7)
    elif n+1 <= N:
        seen[n] = (seen[n]+dfs(n+1))%(10**9+7)

    return seen[n]

N,L = map(int,input().split())
seen = [0]*(N+1)
print(dfs(0))