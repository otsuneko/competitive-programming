N = int(input())
P = list(map(int,input().split()))

mi = P[0]
ans = 0
for p in P:
    if mi >= p:
        ans += 1
    mi = min(mi,p)
print(ans)