N,M = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(M)]

pair = set()
for i in range(M):
    for j in range(N-1):
        pair.add((min(A[i][j],A[i][j+1]), max(A[i][j],A[i][j+1])))

cnt = 0
for i in range(1,N):
    for j in range(i+1,N+1):
        if (i,j) not in pair:
            cnt += 1
print(cnt)