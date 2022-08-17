K,N = map(int,input().split())
A = list(map(int,input().split()))

ans = A[N-1]-A[0]
for i in range(N-1):
    ans = min(ans,A[i]+K-A[i+1])
print(ans)