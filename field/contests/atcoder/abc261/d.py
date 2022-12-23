from collections import defaultdict

N,M = map(int,input().split())
X = list(map(int,input().split()))
bonus = defaultdict(int)
for _ in range(M):
    c,y = map(int,input().split())
    bonus[c] = y

dp = [[0]*(N+1) for _ in range(N+1)]
dp[1][1] = X[0] + bonus[1]

for i in range(1,N):
    ma = 0
    for j in range(N):
        # 表の場合
        if dp[i][j] > 0:
            dp[i+1][j+1] = dp[i][j] + X[i] + bonus[j+1]
        ma = max(ma,dp[i][j])
        # 裏の場合
        dp[i+1][0] = ma

print(max(dp[N]))