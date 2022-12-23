import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,W = map(int,input().split())
goods = [list(map(int,input().split())) for _ in range(N)]

dp = [[0]*(W+1) for i in range(N+1)]

for i in range(N):
    for j in range(W+1):
        if j-goods[i][0] >= 0:
            dp[i][j] = max(dp[i-1][j], dp[i-1][j-goods[i][0]] + goods[i][1])
        else:
            dp[i][j] = dp[i-1][j]

print(dp[N-1][W])