N =int(input())
mod = 998244353

dp = [[0]*9 for _ in range(N)]

for i in range(9):
    dp[0][i] = 1

for i in range(N-1):
    for j in range(9):
        dp[i+1][j] = (dp[i+1][j]+dp[i][j])%mod
        if 0 <= j-1:
            dp[i+1][j] = (dp[i+1][j]+dp[i][j-1])%mod
        if j+1 < 9:
            dp[i+1][j] = (dp[i+1][j]+dp[i][j+1])%mod

print(sum(dp[N-1])%mod)