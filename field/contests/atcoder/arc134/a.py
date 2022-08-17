from math import ceil


N,L,W =map(int,input().split())
A = list(map(int,input().split())) + [L]

ans = 0
cur = 0
for a in A:
    if cur < a:
        n = -(-(a-cur)//W)
        ans += n
        cur = max(cur + n*W, a + W)
    else:
        cur = max(cur, a + W)

print(ans)

