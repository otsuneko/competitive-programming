import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())

MOD = 998244353

dp = [[0]*2 for _ in range(N+1)]
dp[0][0] = M-1 # i人目が1人目と被ってない
dp[0][1] = 0 # i人目が1人目と被ってる

for i in range(N):
    dp[i+1][0] = (dp[i+1][0] + dp[i][1] * (M-1))%MOD

    dp[i+1][1] = (dp[i+1][1] + dp[i][0])%MOD

    dp[i+1][0] = (dp[i+1][0] + dp[i][0] * (M-2))%MOD

print(dp)
print(dp[N][0])