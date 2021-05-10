N,M = map(int,input().split())

A = [list(map(int,input().split())) for _ in range(N)]
ans = 0
for i in range(M):
    for j in range(i+1,M):
        total_score = 0
        for k in range(N):
            total_score += max(A[k][i],A[k][j])
        ans = max(ans, total_score)
print(ans)