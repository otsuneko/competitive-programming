N,W = map(int,input().split())
cheese = [list(map(int,input().split())) for _ in range(N)]
cheese.sort(reverse=True)

ans = 0
for i in range(N):
    if W - cheese[i][1] >= 0:
        ans += cheese[i][0]*cheese[i][1]
        W -= cheese[i][1]
    else:
        ans += cheese[i][0]*min(W,cheese[i][1])
        W = 0
        break

print(ans)