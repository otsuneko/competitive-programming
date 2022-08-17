N,M,K =map(int,input().split())
mod = 998244353

dp = [[0]*(K+1) for _ in range(N)]

for m in range(1,M+1):
    dp[0][m] = 1

for n in range(N-1):
    for k in range(1,K+1):
        for m in range(1,M+1):
            if k+m <= K:
                dp[n+1][k+m] = (dp[n+1][k+m] + dp[n][k])%mod

# print(*dp, sep="\n")

ans = 0
for k in range(1,K+1):
    ans = (ans+dp[N-1][k])%mod
print(ans)