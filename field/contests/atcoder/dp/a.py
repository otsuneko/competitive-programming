N = int(input())
H = list(map(int,input().split()))

dp = [float("INF")]*N

dp[0] = 0
dp[1] = abs(H[1]-H[0])
for i in range(N-2):
    dp[i+2] = min(dp[i+1]+abs(H[i+2]-H[i+1]), dp[i] + abs(H[i+2]-H[i]))

print(dp[N-1])