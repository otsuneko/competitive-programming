N = int(input())
S = input()
T = "atcoder"
dp = [[0]*(7+1) for i in range(N+1)]
dp[0][0] = 1

for i in range(N):
    for j in range(8):
        if j < 7 and S[i] == T[j]:
            dp[i+1][j+1] += dp[i][j]
        dp[i+1][j] += dp[i][j]

# print(*dp, sep="\n")
print(dp[N][7]%(10**9+7))