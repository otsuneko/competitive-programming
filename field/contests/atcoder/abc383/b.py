import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W,D = map(int,input().split())
S = [list(input()) for _ in range(H)]

import itertools

ans = 0
for cmb in itertools.combinations(range(H*W),2):
    y1,x1 = cmb[0]//W, cmb[0]%W
    y2,x2 = cmb[1]//W, cmb[1]%W

    if not (S[y1][x1] == "." and S[y2][x2] == "."):
        continue

    s = set()

    for y in range(y1-D,y1+D+1):
        for x in range(x1-D,x1+D+1):
            if 0<=y<H and 0<=x<W and S[y][x] == "." and abs(y1-y) + abs(x1-x) <= D:
                s.add((y,x))

    for y in range(y2-D,y2+D+1):
        for x in range(x2-D,x2+D+1):
            if 0<=y<H and 0<=x<W and S[y][x] == "." and abs(y2-y) + abs(x2-x) <= D:
                s.add((y,x))

    ans = max(ans, len(s))
print(ans)
