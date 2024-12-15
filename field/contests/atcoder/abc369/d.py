import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int, input().split()))

dp = [[0] * 2 for _ in range(N+1)]

for i in range(N):
    dp[i+1][0] = max(dp[i+1][0], dp[i][1] + A[i], dp[i][0])

    if i > 0:
        if dp[i][0] > 0:
            dp[i+1][1] = max(dp[i+1][1], dp[i][0] + A[i]*2, dp[i][1])
        else:
            dp[i+1][1] = max(dp[i+1][1], dp[i][0] + A[i], dp[i][1])

print(max(dp[N]))
