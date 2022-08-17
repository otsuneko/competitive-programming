H, W = map(int, input().split())
C = []
for _ in range(H):
    C.append(list(input()))
ans = []
for _ in range(H):
    ans.append([-1] * W)
ans[0][0] = 1

for i in range(H):
    for j in range(W):
        if C[i][j] == "#":
            continue

        if j - 1 >= 0 and ans[i][j - 1] != -1:
            ans[i][j] = max(ans[i][j], ans[i][j - 1] + 1)
        
        if i - 1 >= 0 and ans[i - 1][j] != -1:
            ans[i][j] = max(ans[i][j], ans[i - 1][j] + 1)

ma = 1
for i in range(H):
    for j in range(W):
        ma = max(ma, ans[i][j])

print(ma)

# H,W = map(int,input().split())
# C = [list(input()) for _ in range(H)]

# dp = [[0]*(W) for _ in range(H)]
# ans = dp[0][0] = 1

# for y in range(H):
#     for x in range(W):
#         if dp[y][x] == 0:
#             continue

#         if y+1 < H and C[y+1][x] == ".":
#             dp[y+1][x] = max(dp[y+1][x], dp[y][x]+1)
#             ans = max(ans,dp[y+1][x])

#         if x+1 < W and C[y][x+1] == ".":
#             dp[y][x+1] = max(dp[y][x+1], dp[y][x]+1)
#             ans = max(ans,dp[y][x+1])

# # print(*dp, sep="\n")
# print(ans)