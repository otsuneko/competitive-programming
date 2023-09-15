import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W,N = map(int,input().split())
halls = [list(map(int,input().split())) for _ in range(N)]
grid = [[1]*W for _ in range(H)]
for y,x in halls:
    grid[y-1][x-1] = 0

# print(*grid, sep="\n")
dp = [[0]*W for _ in range(H)]

ans = 0
for i in range(H):
    for j in range(W):
        if grid[i][j] == 0:
            dp[i][j] = 0
        else:
            dp[i][j] = 1 + min(dp[i-1][j], min(dp[i][j-1], dp[i-1][j-1]))
        
        ans += dp[i][j]

print(ans)