N,W =map(int,input().split())
A =list(map(int,input().split()))

ans = set()
for i in range(N):
    if A[i] <= W:
        ans.add(A[i])
    for j in range(i+1,N):
        if A[i]+A[j] <= W:
            ans.add(A[i]+A[j])
        for k in range(j+1,N):
            if A[i]+A[j]+A[k] <= W:
                ans.add(A[i]+A[j]+A[k])
print(len(ans))