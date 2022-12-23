N = int(input())
happiness = [list(map(int,input().split())) for _ in range(N)]

dp = [[0]*3 for i in range(N)]
dp[0][0] = happiness[0][0]
dp[0][1] = happiness[0][1]
dp[0][2] = happiness[0][2]

for i in range(N-1):
    dp[i+1][0] = max(dp[i][1] + happiness[i+1][0], dp[i][2] + happiness[i+1][0])
    dp[i+1][1] = max(dp[i][0] + happiness[i+1][1], dp[i][2] + happiness[i+1][1])
    dp[i+1][2] = max(dp[i][0] + happiness[i+1][2], dp[i][1] + happiness[i+1][2])

print(max(dp[N-1]))
