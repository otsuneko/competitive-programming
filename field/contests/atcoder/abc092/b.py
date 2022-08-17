N = int(input())
D,X = map(int,input().split())
A = [int(input()) for _ in range(N)]

ans = X
for i in range(N):
    d = 1
    mul = 1
    while d <= D:
        ans += 1
        d = mul * A[i] + 1
        mul += 1
print(ans)