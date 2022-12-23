N,M = map(int,input().split())
A,B,C,D,E,F = map(int,input().split())
mod = 998244353
obstacle = set()
for _ in range(M):
    x,y = map(int,input().split())
    obstacle.add((x,y))

dp = [[[0]*(N+1) for _ in range(N+1)] for _ in range(N+1)]
dp[0][0][0] = 1

for n in range(N):
    for w1 in range(n+1):
        for w2 in range(n+1):
            nx,ny = w1*A + w2*C + (n-w1-w2)*E, w1*B + w2*D + (n-w1-w2)*F
            if (nx+A,ny+B) not in obstacle:
                dp[n+1][w1+1][w2] = (dp[n+1][w1+1][w2] + dp[n][w1][w2])%mod

            if (nx+C,ny+D) not in obstacle:
                dp[n+1][w1][w2+1] = (dp[n+1][w1][w2+1] + dp[n][w1][w2])%mod

            if (nx+E,ny+F) not in obstacle:
                dp[n+1][w1][w2] = (dp[n+1][w1][w2] + dp[n][w1][w2])%mod

ans = 0
for w1 in range(N+1):
    for w2 in range(N+1):
        ans = (ans + dp[N][w1][w2])%mod
print(ans)