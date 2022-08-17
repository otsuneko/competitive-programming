def pos(x, n, m):
    if n == 0:
        return 1
    res = pos(x*x%m, n//2, m)
    if n%2 == 1:
        res = res*x%m
    return res

N,P = map(int,input().split())
mod = 10**9+7

ans = (P-1) * pos(P-2,N-1,mod) % mod
print(ans)