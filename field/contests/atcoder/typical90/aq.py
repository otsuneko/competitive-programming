from collections import deque

H,W = map(int,input().split())
sy,sx = map(int,input().split())
ty,tx = map(int,input().split())
sy,sx,ty,tx = sy-1,sx-1,ty-1,tx-1
maze = [list(input()) for _ in range(H)]

# turn[y][x][d]: (x,y)にdの方向([U,R,D,L])から入ってきたときの最小方向転換数
turn = [[10**6]*4 for _ in range(H*W)]
que = deque()
for d in range(4):
    turn[sy*W+sx][d] = 0
    que.append((sy*W+sx,d))

move = ((-1, 0), (0, 1), (1, 0), (0, -1)) # URDL
while que:
    yx,pre_d = que.popleft()
    y,x = yx//W,yx%W
    for i,[dy,dx] in enumerate(move): #どの方向を向いて進むか
        ny,nx = y+dy, x+dx
        if 0 <= ny < H and 0 <= nx < W and maze[ny][nx] != "#":
            nyx = ny*W+nx
            if i == pre_d:
                if turn[nyx][i] > turn[yx][i]:
                    turn[nyx][i] = turn[yx][i]
                    que.appendleft((ny*W+nx,i))
                    for dir2 in range(4):
                        if dir2 != i:
                            turn[nyx][dir2] = min(turn[nyx][dir2], turn[nyx][i] + 1)
            else:
                if turn[nyx][i] > turn[yx][pre_d] + 1:
                    turn[nyx][i] = turn[yx][pre_d] + 1
                    que.append((ny*W+nx,i))
                    for dir2 in range(4):
                        if dir2 != i:
                            turn[nyx][dir2] = min(turn[nyx][dir2], turn[nyx][i] + 1)

print(min(turn[ty*W+tx]))