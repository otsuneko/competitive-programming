def calc_point(y,x):
    if A[y][x] == "+":
        return 1
    else:
        return 0

H,W = map(int,input().split())
A = [list(input()) for _ in range(H)]

dp = [[0]*(W) for i in range(H)]

for y in reversed(range(H)):
    for x in reversed(range(W)):
        if y == H-1 and x == W-1:
            continue
        elif x+y & 1:
            if y == H-1:
                dp[y][x] = dp[y][x+1]-calc_point(y,x+1)
            elif x == W-1:
                dp[y][x] = dp[y+1][x]-calc_point(y+1,x)
            else:
                dp[y][x] = min(dp[y+1][x]-calc_point(y+1,x), dp[y][x+1]-calc_point(y,x+1))
        else:
            if y == H-1:
                dp[y][x] = dp[y][x+1]+calc_point(y,x+1)
            elif x == W-1:
                dp[y][x] = dp[y+1][x]+calc_point(y+1,x)
            else:
                dp[y][x] = max(dp[y+1][x]+calc_point(y+1,x), dp[y][x+1]+calc_point(y,x+1))

# print(*dp, sep="\n")
if dp[0][0] > 0:
    print("Takahashi")
elif dp[0][0] == 0:
    print("Draw")
else:
    print("Aoki")