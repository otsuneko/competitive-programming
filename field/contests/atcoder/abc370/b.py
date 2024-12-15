import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = [list(map(int,input().split())) for _ in range(N)]

ans = 0
for j in range(N):
    i = ans
    if i >= j:
        ans = A[i][j] - 1
    else:
        ans = A[j][i] - 1
print(ans+1)
