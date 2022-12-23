N,K = map(int,input().split())
mod = 10**9+7

ans = 0
for i in range(K,N+2):
    ans = (ans + (i*(2*N+1-i)//2) - (i*(i-1)//2) + 1)%mod
print(ans)