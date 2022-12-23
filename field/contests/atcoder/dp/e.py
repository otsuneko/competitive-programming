import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,W = map(int, input().split())
goods = [list(map(int,input().split())) for _ in range(N)]
dp = [[INF for i in range(10**5+1)] for j in range(N+1)]
dp[0][0] = 0

for i in range(N):
    for j in range(10**5+1):
        if j >= goods[i][1]:
            dp[i+1][j] = min(dp[i][j-goods[i][1]] + goods[i][0], dp[i][j])
        else:
            dp[i+1][j] = dp[i][j]

ans = 0
for i,n in enumerate(dp[N]):
    if n <= W:
        ans = i
print(ans)