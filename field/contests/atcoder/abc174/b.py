N,D = map(int,input().split())
pos = [list(map(int,input().split())) for _ in range(N)]

ans = 0
for p in pos:
    if (p[0]**2 + p[1]**2)**0.5 <= D:
        ans += 1
print(ans)