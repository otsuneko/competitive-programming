N = int(input())

ans = float("INF")
cnt = 0
N2 = N
while N2 != 1:
    N2//=2
    cnt += 1
    q,r = divmod(N,2**cnt)
    ans = min(ans, q+r+cnt)

if ans == float("INF"):
    print(1)
else:
    print(ans)
