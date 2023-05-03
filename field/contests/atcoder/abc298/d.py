import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
from collections import deque

def pos(x, n, m):
    if n == 0:
        return 1
    res = pos(x*x%m, n//2, m)
    if n%2 == 1:
        res = res*x%m
    return res

Q = int(input())
mod = 998244353

S = deque([1])
n = 1

for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        x = query[1]
        S.append(x)
        n *= 10
        n += x
        n %= mod
    elif query[0] == 2:
        n = (n - int(S[0]) * pos(10,len(S)-1,mod)) % mod
        S.popleft()
    elif query[0] == 3:
        n %= mod
        print(n)