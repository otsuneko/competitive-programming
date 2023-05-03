N = int(input())
A = list(map(int,input().split()))

B = [0]*N
for i in range(1,N):
    B[i] = B[i-1] + A[(i-1)//2]

dp = [[-1]*(N+1) for _ in range(N+1)]
dp[0][0] = 0

for i in range(N-1):
    for j in range(N):
        if dp[i][j] < 0:
            continue
        dp[i+1][j+1] = max(dp[i+1][j+1], dp[i][j])
        dp[i+1][0] = max(dp[i+1][0], dp[i][j] + B[j])