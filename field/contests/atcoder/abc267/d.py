N,M = map(int,input().split())
A = list(map(int,input().split()))

# dp[i個までのうち][j個使う]
dp = [[-10**18]*(M+1) for _ in range(N+1)]
dp[0][0] = 0

for i in range(N):
    for j in range(M):
        dp[i+1][j] = max(dp[i+1][j], dp[i][j])
        dp[i+1][j+1] = max(dp[i+1][j+1], dp[i][j+1], dp[i][j] + A[i]*(j+1))

# print(*dp, sep="\n")

print(dp[N][M])