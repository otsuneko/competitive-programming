
dir = {"U":(-1,0), "R":(0,1), "D":(1,0), "L":(0,-1)}
H,W = map(int,input().split())
grid =  [list(input()) for _ in range(H)]
path = set()

cur = [0,0]
while 1:
    y,x = cur
    ny,nx = y+dir[grid[y][x]][0],x+dir[grid[y][x]][1]
    if 0<=ny<H and 0<=nx<W:
        cur = [ny,nx]
        if tuple(cur) in path:
            print(-1)
            exit()
    else:
        print(cur[0]+1,cur[1]+1)
        exit()
    path.add(tuple(cur))
