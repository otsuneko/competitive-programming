N = int(input())
P = list(map(float,input().split()))

# [N][K]:N枚投げて表がK枚
dp = [[0]*(N+1) for _ in range(N+1)]
dp[0][0] = 1

for i in range(N):
    for j in range(i+1):
        # i枚目が表
        dp[i+1][j+1] += dp[i][j] * P[i]
        # i枚目が裏
        dp[i+1][j] += dp[i][j] * (1-P[i])

# print(dp)

ans = 0
for i in range(-(-(N)//2),N+1):
    ans += dp[N][i]
print(ans)