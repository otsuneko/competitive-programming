from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
from collections import defaultdict

H,W,rs,cs = map(int,input().split())
N = int(input())
wall = [list(map(int,input().split())) for _ in range(N)]
Q = int(input())
query = [list(map(str,input().split())) for _ in range(Q)]

li_x = defaultdict(list)
li_y = defaultdict(list)

for y,x in wall:
    insort(li_x[x],y)
    insort(li_y[y],x)

cy,cx = rs,cs
for i in range(Q):
    d,l = query[i][0],int(query[i][1])

    if d == "L":
        if len(li_y[cy]) > 0:
            idx = bisect(li_y[cy],cx)
            if idx == 0:
                l = max(0, min(l, cx-1))
            else:
                l = max(0, min(l, cx - li_y[cy][idx-1] - 1))
        else:
            l = max(0, min(l, cx-1))
        cx -= l
    elif d == "R":
        if len(li_y[cy]) > 0:
            idx = bisect(li_y[cy],cx)
            if idx == len(li_y[cy]):
                l = max(0, min(l, W-cx))
            else:
                l = max(0, min(l, li_y[cy][idx] - cx - 1))
        else:
            l = max(0, min(l, W-cx))
        cx += l
    elif d == "U":
        if len(li_x[cx]) > 0:
            idx = bisect(li_x[cx],cy)
            if idx == 0:
                l = max(0, min(l, cy-1))
            else:
                l = max(0, min(l, cy - li_x[cx][idx-1] - 1))
        else:
            l = max(0, min(l, cy-1))
        cy -= l
    elif d == "D":
        if len(li_x[cx]) > 0:
            idx = bisect(li_x[cx],cy)
            if idx == len(li_x[cx]):
                l = max(0, min(l, H-cy))
            else:
                l = max(0, min(l, li_x[cx][idx] - cy - 1))
        else:
            l = max(0, min(l, H-cy))
        cy += l

    print(cy,cx)