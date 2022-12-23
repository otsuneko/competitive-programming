N,M = map(int,input().split())

dp = [[-1]*N for _ in range(N)]
dp[0][0] = 0

for _ in range(100):
    for i in range(N):
        for j in range(N):
            if dp[i][j] == -1:
                continue
            