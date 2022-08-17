N,x = map(int,input().split())
A = list(map(int,input().split()))

ans = 0
for i in range(N):
    if A[i] > x:
        ans += A[i]-x
        A[i] = x

for i in range(1,N):
    if A[i] + A[i-1] > x:
        ans += A[i]+A[i-1]-x
        A[i] = x-A[i-1]
print(ans)