N,K,X =map(int,input().split())
A =list(map(int,input().split()))
A.sort(reverse=True)

for i,a in enumerate(A):
    k = a//X
    if K >= k:
        K -= k
        A[i] = max(0,A[i]-k*X)

ans = 0
A.sort(reverse=True)
for i,a in enumerate(A):
    if K > 0:
        K -= 1
        A[i] = max(0,A[i]-X)

for a in A:
    ans += a

print(ans)