N = int(input())
A = list(map(int,input().split()))
M = int(input())
B = set(list(map(int,input().split())))
X = int(input())

dp = [False]*(X+1)
dp[0] = True

for j in range(X+1):
    if j in B or dp[j] == False:
        continue
    for i in range(N):
        if j + A[i] <= X:
            dp[j+A[i]] = True

# print(dp)
print(["No","Yes"][dp[X]])