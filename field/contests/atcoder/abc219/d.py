N = int(input())
X,Y = map(int,input().split())
bento = []
sum_A = 0
sum_B = 0
num = 0
used = [True]*N
for _ in range(N):
    A,B = map(int,input().split())
    sum_A += A
    sum_B += B
    num += 1
    bento.append([A,B])

if sum_A < X or sum_B < Y:
    print(-1)
    exit()

dp = [[[0,0] for _ in range(sum_A+1)] for _ in range(N+1)]

ans = 10**18
for i in range(N):
    for j in range(sum_A+1):
        dp[i][j] = 

# print(*dp, sep="\n")
print(ans)