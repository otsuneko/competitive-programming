import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')
from functools import lru_cache

@lru_cache(maxsize=100000)
def dfs(n):
    if n == 0:
        return 0
    res1 = dfs(n//A) + X
    res2 = (dfs(n//2)+dfs(n//3)+dfs(n//4)+dfs(n//5)+dfs(n//6))/5 + Y*6/5
    return min(res1,res2)

N,A,X,Y = map(int,input().split())
print(dfs(N))
