N,K = map(int,input().split())
H = list(map(int,input().split()))

dp = [float("INF")]*N

dp[0] = 0
for i in range(1,N):
    for j in range(1,K+1):
        if i-j >= 0:
            dp[i] = min(dp[i-j]+abs(H[i]-H[i-j]), dp[i])
print(dp[N-1])