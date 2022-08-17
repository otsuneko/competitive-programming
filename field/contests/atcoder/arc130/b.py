H,W,C,Q = map(int,input().split())
color = [0]*C
paint = []
sx, sy = [], []
cnt_y = cnt_x = 0
for i in range(Q):
    t,n,c = map(int,input().split())
    n,c = n-1,c-1
    if t == 1:
        sy.append(n)
        cnt_y += 1
    else:
        sx.append(n)
        cnt_x += 1

    paint.append((t,n,c))

paint = paint[::-1]
sx.sort()
sy.sort()

used_row = set()
used_col = set()
num_row = num_col = 0
for t,n,c in paint:
    if t == 1:
        if n not in used_row:
            num_row += 1
            color[c] += W - num_col
            used_row.add(n)
    else:
        if n not in used_col:
            num_col += 1
            color[c] += H - num_row
            used_col.add(n)

print(*color)