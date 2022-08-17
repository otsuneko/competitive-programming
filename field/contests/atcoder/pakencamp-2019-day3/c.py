N,M =map(int,input().split())
A =[list(map(int,input().split())) for _ in range(N)]

ans = 0
for t1 in range(M):
    for t2 in range(t1+1,M):
        score = 0
        for n in range(N):
            score += max(A[n][t1],A[n][t2])
        ans = max(ans,score)
print(ans)