import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
cities = [list(map(int, input().split())) for _ in range(N)]

dp = [[INF] * N for _ in range(1 << N)]
dp[1][0] = 0

for s in range(1 << N):
    for i in range(N):
        if dp[s][i] == INF:
            continue
        for j in range(N):
            if s >> j & 1:
                continue
            x1,y1,z1 = cities[i]
            x2,y2,z2 = cities[j]
            d = abs(x2 - x1) + abs(y2 - y1) + max(0, z2 - z1)
            dp[s | 1 << j][j] = min(dp[s | 1 << j][j], dp[s][i] + d)

ans = INF
for i in range(1,N):
    x1,y1,z1 = cities[i]
    x2,y2,z2 = cities[0]
    d = abs(x2 - x1) + abs(y2 - y1) + max(0, z2 - z1)
    ans = min(ans, dp[(1 << N) - 1][i] + d)
print(ans)
