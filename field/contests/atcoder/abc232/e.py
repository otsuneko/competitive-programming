H,W,K = map(int,input().split())
x1,y1,x2,y2 = map(int,input().split())
mod = 998244353

dp = [0]*4

if x1 == x2 and y1 == y2:
    dp[0] += 1
elif x1 == x2:
    dp[1] += 1
elif y1 == y2:
    dp[2] += 1
else:
    dp[3] += 1

for _ in range(K):
    nxt = [0]*4

    nxt[1] += dp[0]*(W-1)
    nxt[2] += dp[0]*(H-1)

    nxt[0] += dp[1]
    nxt[1] += dp[1]*(W-2)
    nxt[3] += dp[1]*(H-1)

    nxt[0] += dp[2]
    nxt[2] += dp[2]*(H-2)
    nxt[3] += dp[2]*(W-1)

    nxt[1] += dp[3]
    nxt[2] += dp[3]
    nxt[3] += dp[3]*(H-2 + W-2)

    for i in range(4):
        dp[i] = nxt[i]%mod

print(dp[0])