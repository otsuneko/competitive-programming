import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W,Y = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]

Q = [[] for _ in range(Y+1)]

for y in range(H):
    for x in range(W):
        if (y in [0,H-1] or x in [0,W-1]) and A[y][x] <= Y:
            Q[A[y][x]].append((y,x))
            A[y][x] = INF

field_cnt = H*W
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1]) #縦横移動
for year in range(1,Y+1):
    for y,x in Q[year]:
        for dy,dx in MOVE:
            ny,nx = y+dy,x+dx
            if 0 <= ny < H and 0 <= nx < W and A[ny][nx] <= Y:
                Q[max(year,A[ny][nx])].append((ny,nx))
                A[ny][nx] = INF

    field_cnt -= len(Q[year])
    print(field_cnt)
