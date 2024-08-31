import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = input()

# グーが0、チョキが1、パーが2
dp = [[0]*3 for _ in range(N)]
if S[0] == "R":
    dp[0][0] = 0
    dp[0][1] = 1
elif S[0] == "P":
    dp[0][1] = 0
    dp[0][2] = 1
else:
    dp[0][0] = 1
    dp[0][2] = 0

for i in range(1,N):
    if S[i] == "R":
        # あいこ
        dp[i][0] = max(dp[i-1][1], dp[i-1][2])
        # 勝ち
        dp[i][1] = max(dp[i-1][0], dp[i-1][2])+1
    elif S[i] == "P":
        # あいこ
        dp[i][1] = max(dp[i-1][0], dp[i-1][2])
        # 勝ち
        dp[i][2] = max(dp[i-1][0], dp[i-1][1])+1
    else:
        # あいこ
        dp[i][2] = max(dp[i-1][0], dp[i-1][1])
        # 勝ち
        dp[i][0] = max(dp[i-1][1], dp[i-1][2])+1

print(max(dp[N-1]))
