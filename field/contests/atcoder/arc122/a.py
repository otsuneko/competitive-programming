mod = 10**9+7
N = int(input())
A = list(map(int,input().split()))

dp = [[0]*2 for _ in range(N)]
dp[0][0] = A[0]
fib = [1,1]

ans = 0
for i in range(N-1):
    # dp[i][1]: A[i]の前が"+"、dp[i][0]: A[i]の前が"-"
    if i == 0:
        dp[i+1][1] = (dp[i][0] + A[i+1])%mod
        dp[i+1][0] = dp[i][0] - A[i+1]
    else:
        dp[i+1][1] = (dp[i][1] + dp[i][0] + A[i+1] * fib[0])%mod
        dp[i+1][0] = dp[i][1] - A[i+1] * fib[1]
    fib = [(fib[0]+fib[1])%mod, fib[0]]

# print(dp)
print(sum(dp[N-1])%mod)