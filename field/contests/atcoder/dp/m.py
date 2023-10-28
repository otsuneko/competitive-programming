N,K = map(int,input().split())
A = list(map(int,input().split()))
MOD = 10**9+7

dp = [[0]*(K+1) for _ in range(N+1)]
dp[0][0] = 1

for i in range(N):
    for j in range(K+1):
        for k in range(A[i]+1):
            if dp[i][j] > 0:
                dp[i+1][j]


# for i in range(N):
#     sum_dp = [0]*(K+2)
#     for j in range(K+1):
#         sum_dp[j+1] = (sum_dp[j] + dp[i][j])%MOD
    
#     for j in range(K+1):
#         dp[i+1][j] = (sum_dp[j+1] - sum_dp[j-min(j,A[i])])%MOD

# print(dp[N][K])