N,X = map(int,input().split())

A = list(map(int,input().split()))

ans = "Yes"
for i in range(N):
    X -= A[i]

X += N//2
if X < 0:
    ans = "No"

print(ans)