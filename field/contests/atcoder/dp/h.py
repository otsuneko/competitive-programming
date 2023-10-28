H,W = map(int,input().split())
A = [list(input()) for _ in range(H)]

MOD = 10**9+7

dp = [[0]*W for _ in range(H)]
dp[0][0] = 1

for h in range(H):
    for w in range(W):
        if w+1 < W and A[h][w+1] == ".":
            dp[h][w+1] = (dp[h][w+1] + dp[h][w])%MOD
        if h+1 < H and A[h+1][w] == ".":
            dp[h+1][w] = (dp[h+1][w] + dp[h][w])%MOD

# print(dp)
print(dp[H-1][W-1])