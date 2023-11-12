import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
P = list(map(int,input().split()))

# 今i番目まで見ていて、K番目の要素としてiを選ぶ時
dp = [[-1]*(N+1) for _ in range(N+1)]
for i in range(N):
    dp[i][0] = 0

for i in range(1,N+1):
    for k in range(1,N-i+1):
        dp[i][k] = dp[i-1][k-1]
        if dp[i-1][k-1] != -1:
            dp[i][k] = max(dp[i][k], dp[i-1][k-1] + (0.9)**k * P[i])

print(dp)