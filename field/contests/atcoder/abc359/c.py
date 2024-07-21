import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

sx,sy = map(int,input().split())
tx,ty = map(int,input().split())

if sy%2 == 0:
    if sx%2 == 0:
        sx += 1
else:
    if sx%2 == 1:
        sx += 1

if ty%2 == 0:
    if tx%2 == 0:
        tx += 1
else:
    if tx%2 == 1:
        tx += 1

dy = abs(ty-sy)
if abs(tx-sx) <= dy:
    dx = 0
else:
    dx = abs(tx-sx) - dy
    dx //= 2
ans = dy + dx
print(ans)
