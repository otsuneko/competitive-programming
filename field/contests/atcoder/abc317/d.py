import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
votes = [list(map(int,input().split())) for _ in range(N)]

seats = 0
for x,y,z in votes:
    seats += z
seats = -(-(seats)//2)

dp = [[INF]*(seats+1) for _ in range(N+1)]
dp[0][0] = 0

for i in range(N):
    for j in range(seats+1):
        x,y,z = votes[i]
        # 奪う
        if x < y and dp[i][j] != INF:
            diff = -(-(x+y)//2) - x
            dp[i+1][min(seats,j+z)] = min(dp[i+1][min(seats,j+z)], dp[i][j] + diff)

        # 奪わない
        if x < y and dp[i][j] != INF:
            dp[i+1][j] = min(dp[i+1][j],dp[i][j])
        
        # 奪う必要なし
        if x > y and dp[i][j] != INF:
            dp[i+1][min(seats,j+z)] = min(dp[i+1][min(seats,j+z)],dp[i][j])

print(dp[N][seats])