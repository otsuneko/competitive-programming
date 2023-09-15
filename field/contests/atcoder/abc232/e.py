import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W,K = map(int,input().split())
sx,sy,tx,ty = map(int,input().split())
MOD = 998244353

# 0:xもyも違う、1:xは同じ、2:yは同じ、3:xもyも同じ
dp = [[0]*4 for _ in range(K+1)]

if sx == tx:
    if sy == ty:
        dp[0][3] = 1
    else:
        dp[0][1] = 1
else:
    if sy == ty:
        dp[0][2] = 1
    else:
        dp[0][0] = 1

for i in range(K):
    dp[i+1][0] = (dp[i][0]*(H-2) + dp[i][0]*(W-2) + dp[i][1]*(H-1) + dp[i][2]*(W-1)) % MOD
    dp[i+1][1] = (dp[i][0] + dp[i][1]*(W-2) + dp[i][3]*(W-1)) % MOD
    dp[i+1][2] = (dp[i][0] + dp[i][2]*(H-2) + dp[i][3]*(H-1)) % MOD
    dp[i+1][3] = (dp[i][1] + dp[i][2]) % MOD

# print(*dp, sep="\n")

print(dp[K][3])