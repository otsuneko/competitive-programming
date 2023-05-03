N,X = map(int,input().split())
coins = [list(map(int,input().split())) for _ in range(N)]

dp = [[False]*(X+1) for _ in range(N+1)]
for i in range(N+1):
    dp[i][0] = True

for i in range(N):
    for j in range(X+1):
        if dp[i][j] == False:
            continue
        dp[i+1][j] = dp[i][j]
        for k in range(1,coins[i][1]+1):
            if j+k*coins[i][0] <= X:
                dp[i+1][j+k*coins[i][0]] = True

print(["No","Yes"][dp[N][X]])