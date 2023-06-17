H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]

ma = 0
mx,my = 0,0
move = ([1, 0], [-1, 0], [0, 1], [0, -1])
for y in range(H):
    for x in range(W):
        if S[y][x] != ".":
            continue
        cnt = 0
        for dy,dx in move:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and S[ny][nx] == "#":
                cnt += 1
        if cnt > ma:
            ma = cnt
            my,mx = y+1,x+1
print(my,mx)