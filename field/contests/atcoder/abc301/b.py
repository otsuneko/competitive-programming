N = int(input())
A = list(map(int,input().split()))

ans = []
for i in range(N-1):
    if A[i+1] > A[i]:
        ans.append(A[i])
        for i in range(A[i]+1,A[i+1]):
            ans.append(i)
    elif A[i+1] < A[i]:
        ans.append(A[i])
        for i in range(A[i]-1,A[i+1],-1):
            ans.append(i)
ans.append(A[N-1])
print(*ans)