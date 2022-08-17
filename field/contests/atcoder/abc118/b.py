N,M = map(int,input().split())
like = [0]*M
for _ in range(N):
    tmp = list(map(int,input().split()))
    for t in tmp[1:]:
        like[t-1] += 1

ans = 0
for i in range(M):
    if like[i] == N:
        ans += 1
print(ans)