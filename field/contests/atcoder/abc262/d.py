import json


N = int(input())
A = list(map(int,input().split()))
mod = 998244353

limod = [[0]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        limod[i][j] = A[i]%(j+1)

inv = list(zip(*limod))

ans = 0
for i in range(N):
    dp = [[[0]*(N+1) for _ in range(N+1)] for _ in range(N+1)]
    dp[0][0][0] = 1
    # 前からj個見てk個選んだ時の合計(mod i)がl
    for j in range(N):
        for k in range(i):
            for l in range(N):
                dp[j+1][k][l] += dp[j][k][l]
                if k!=i:
                    dp[j+1][k+1][(l+A[j])%i] += dp[j][k][l]
    print(*dp, sep="\n")
    for j in range(N):
        ans = (ans + dp[N][j][0])%mod


print(ans)