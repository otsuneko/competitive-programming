N,K = map(int,input().split())
A = list(map(int,input().split()))

# dp[0][K]:太郎君のターンで石が残りK個
# dp[1][K]:二郎君のターンで石が残りK個
# 0:太郎君の勝ち、1:二郎君の勝ち
dp = [False]*(K+1)
dp[0] = False

for i in range(K):
    for j in range(N):
        if i+A[j] <= K:
            dp[i+A[j]] |= not dp[i]

# print(dp)
if dp[K]:
    print("First")
else:
    print("Second")
