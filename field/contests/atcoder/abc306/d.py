N = int(input())
dishes = [list(map(int,input().split())) for _ in range(N)]

# 0が普通　１が毒になってる
dp = [[0]*(2) for _ in range(N+1)]
dp[0][0] = dp[1][0] = 0

for i in range(N):
    if dishes[i][0] == 0:
        # 食べる
        dp[i+1][0] = max(dp[i][0] + dishes[i][1], dp[i][1] + dishes[i][1])
        # 下げる
        dp[i+1][0] = max(dp[i+1][0], dp[i][0])
        dp[i+1][1] = dp[i][1]
    else:
        dp[i+1][0] = dp[i][0]
        dp[i+1][1] = max(dp[i+1][1], dp[i][1], dp[i][0] + dishes[i][1])

# print(dp)
print(max(dp[N][0], dp[N][1]))