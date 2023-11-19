N,K,D = map(int,input().split())
A = list(map(int,input().split()))

dp = [[[-1]*D for _ in range(K+1)] for _ in range(N+1)]
dp[0][0][0] = 0

for i in range(N):
    for k in range(K+1):
        for d in range(D):
            if dp[i][k][d] >= 0:
                # 選ぶ
                if k != K:
                    dp[i+1][k+1][(d+A[i])%D] = max(dp[i+1][k+1][(d+A[i])%D], dp[i][k][d]+A[i])
                # 選ばない
                dp[i+1][k][d] = max(dp[i+1][k][d],dp[i][k][d])

# print(dp)
print(dp[N][K][0])