H,W = map(int,input().split())
mini = 10**18
A = []
for _ in range(H):
    tmp = list(map(int,input().split()))
    A.append(tmp)
    mini = min(mini, min(tmp))

ans = 0
for y in range(H):
    for x in range(W):
        ans += A[y][x] - mini
print(ans)