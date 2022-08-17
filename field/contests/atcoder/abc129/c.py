mod = 10**9+7
N,M = map(int,input().split())
danger = set()
for _ in range(M):
    n = int(input())
    danger.add(n)

dp = [0] * (N+1)
dp[0] = 1

for i in range(N):
    if i+1 not in danger:
        dp[i+1] = (dp[i+1] + dp[i]) % mod
    if i+2 <= N and i+2 not in danger:
        dp[i+2] = (dp[i+2] + dp[i]) % mod

print(dp[N])