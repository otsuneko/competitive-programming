N = int(input())
A = list(map(int,input().split()))
mod = 998244353

ans = 0
# i個使えるうち、j個使っている状態でk番目の要素を見ている
dp = [[[0]*(N+1) for _ in range(N+1)] for _ in range(N+1)]

for i in range(N):
    dp[1][1][i] = 1

for i in range(N):
    for j in range(N):
        for k in range(N):
            dp[j+1][k][l] += dp[j][k][l]


print(*dp, sep="\n")


print(ans)