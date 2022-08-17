S = list(input())
mod = 10**9+7

dp = [[0]*(len(S)+1) for _ in range(9)]
check = ["c","h","o","k","u","d","a","i"]

for i in range(len(S)):
    if S[i] == check[0]:
        dp[0][i] = 1


for i in range(8):
    for j in range(len(S)):
        if S[j] == check[i]:
            dp[i+1][j] = (dp[i][j]+dp[i+1][j-1])%mod
        else:
            dp[i+1][j] = dp[i+1][j-1]%mod

print(dp[8][len(S)-1])