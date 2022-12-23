mod = 998244353
N = int(input())
A = list(map(int,input().split()))

dp = [[0]*10 for _ in range(N)]

dp[0][(A[0]+A[1])%10] = 1
dp[0][(A[0]*A[1])%10] += 1
 
for i in range(2,N):
    for j in range(10):
        dp[i-1][(A[i]+j)%10] = (dp[i-1][(A[i]+j)%10] + dp[i-2][j])%mod
        dp[i-1][(A[i]*j)%10] = (dp[i-1][(A[i]*j)%10] + dp[i-2][j])%mod

for i in range(10):
    print(dp[N-2][i])