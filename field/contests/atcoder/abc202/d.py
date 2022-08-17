A,B,K = map(int,input().split())
dp = [[0]*(B+1) for _ in range(A+1)]
dp[0][0] = 1

ans = ""
for i in range(A+1):
    for j in range(B+1):
        if i > 0:
            dp[i][j] += dp[i-1][j]
        if j > 0:
            dp[i][j] += dp[i][j-1]

while A > 0 and B > 0:
    if K <= dp[A-1][B]:
        ans += "a"
        A -= 1
    else:
        K -= dp[A-1][B]
        ans += "b"
        B -= 1

ans += "a"*A +"b"*B

# print(*dp, sep="\n")
print(ans)



### original code ###
# def nCr(n, r):

#     res = 1
#     for i in range(r):
#         res = (res*(n-i))//(i+1)

#     return res

# A,B,K = map(int,input().split())

# ans = ""
# while A > 0 or B > 0:
#     total_A = nCr(A+B-1,A-1)

#     if A == 0:
#         ans += "b"
#         B -= 1
#     elif B == 0:
#         ans += "a"
#         A -= 1
#     elif total_A < K:
#         ans += "b"
#         B -= 1
#         K -= total_A
#     elif total_A >= K:
#         ans += "a"
#         A -= 1

# print(ans)
