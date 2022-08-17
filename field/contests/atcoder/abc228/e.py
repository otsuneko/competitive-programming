N,K,M = map(int,input().split())
mod = 998244353
p = pow(K,N,mod-1)
ans = pow(M,p,mod)
if M%mod == 0:
    print(0)
else:
    print(ans)