N,K = map(int,input().split())
mod = 10**9+7

if N == 1:
    print(K)
elif N == 2:
    print(K*(K-1)%mod)
else:
    if K < 3:
        print(0)
    else:
        ans = K * (K-1) * pow(K-2,N-2,mod) % mod
        print(ans)