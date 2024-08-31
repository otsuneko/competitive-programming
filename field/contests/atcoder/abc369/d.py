import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int, input().split()))

dp = [[0] * 3 for _ in range(N)]

dp[0][0] = 0
dp[0][1] = A[0]
dp[0][2] = 0

for i in range(1, N):
    dp[i][1] = max(dp[i-1][0] + A[i], dp[i-1][1], dp[i-1][2] + A[i])
    dp[i][2] = max(dp[i-1][1] + 2 * A[i])

ans = max(dp[N-1][0], dp[N-1][1], dp[N-1][2])
print(ans)
