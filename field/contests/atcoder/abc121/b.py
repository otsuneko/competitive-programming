N,M,C = map(int,input().split())
B = list(map(int,input().split()))
A = [list(map(int,input().split())) for _ in range(N)]

ans = 0
for i in range(N):
    su = 0
    for j in range(M):
        su += A[i][j] * B[j]
    if su + C > 0:
        ans += 1
print(ans)