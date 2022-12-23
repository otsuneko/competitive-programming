H,W = map(int,input().split())
grid = [list(input()) for _ in range(H)]
mod = 998244353

seen = [[False]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if seen[y][x]:
            continue
        if grid[y][x] == "R":
            d = 1
            while 1:
                ny,nx = y-d,x+d
                if 0<=ny<H and 0<=nx<W:
                    if grid[ny][nx] == "B":
                        print(0)
                        exit()
                    elif grid[ny][nx] == ".":
                        grid[ny][nx] = "R"
                    seen[ny][nx] = True
                    d += 1
                else:
                    break
            d = 1
            while 1:
                ny,nx = y+d,x-d
                if 0<=ny<H and 0<=nx<W:
                    if grid[ny][nx] == "B":
                        print(0)
                        exit()
                    elif grid[ny][nx] == ".":
                        grid[ny][nx] = "R"
                    seen[ny][nx] = True
                    d += 1
                else:
                    break

        if grid[y][x] == "B":
            d = 1
            while 1:
                ny,nx = y-d,x+d
                if 0<=ny<H and 0<=nx<W:
                    if grid[ny][nx] == "R":
                        print(0)
                        exit()
                    elif grid[ny][nx] == ".":
                        grid[ny][nx] = "B"
                    seen[ny][nx] = True
                    d += 1
                else:
                    break
            d = 1
            while 1:
                ny,nx = y+d,x-d
                if 0<=ny<H and 0<=nx<W:
                    if grid[ny][nx] == "R":
                        print(0)
                        exit()
                    elif grid[ny][nx] == ".":
                        grid[ny][nx] = "B"
                    seen[ny][nx] = True
                    d += 1
                else:
                    break

ans = 1
seen = [[False]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if seen[y][x]:
            continue
        if grid[y][x] == ".":
            ans = ans*2%mod
            d = 1
            while 1:
                ny,nx = y-d,x+d
                if 0<=ny<H and 0<=nx<W:
                    seen[ny][nx] = True
                    d += 1
                else:
                    break
            d = 1
            while 1:
                ny,nx = y+d,x-d
                if 0<=ny<H and 0<=nx<W:
                    seen[ny][nx] = True
                    d += 1
                else:
                    break

print(ans)