H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]

move = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
ans = [[0]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if S[y][x] == "#":
            ans[y][x] = "#"
            continue
        cnt = 0
        for dy,dx in move:
            if 0<=y+dy<H and 0<=x+dx<W:
                if S[y+dy][x+dx] == "#":
                    cnt += 1
        ans[y][x] = str(cnt)

for y in range(H):
    print("".join(ans[y]))