def funcA(Xa, Ya, Xb, Yb):
    a = (Yb - Ya)/(Xb - Xa)
    b = Yb - a * Xb
    return b

N,D,H = map(int,input().split())

tower = []
ans = 0
for _ in range(N):
    d,h = map(int,input().split())
    tower.append((d,h))
    height = funcA(d,h,D,H)
    ans = max(ans, height)
print(ans)