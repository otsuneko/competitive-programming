X,Y,Z = map(int,input().split())
S = input()
N = len(S)
dp = [[0]*2 for _ in range(N+1)] # 1 なら on 0 なら off

for i in range(N):
    if S[i] == "a":
        if i > 0:
            dp[i+1][0] = min(dp[i][0] + X, dp[i][1] + Z+X)
            dp[i+1][1] = min(dp[i][0] + Z+Y, dp[i][1] + Y)
        else:
            dp[i+1][0] = dp[i][0] + X
            dp[i+1][1] = dp[i][0] + Z+Y
    elif S[i] == "A":
        if i > 0:
            dp[i+1][0] = min(dp[i][0] + Y, dp[i][1] + Z+Y)
            dp[i+1][1] = min(dp[i][0] + Z+X, dp[i][1] + X)
        else:
            dp[i+1][0] = dp[i][0] + Y
            dp[i+1][1] = dp[i][0] + Z+X

# print(*dp, sep="\n")

print(min(dp[N][0],dp[N][1]))