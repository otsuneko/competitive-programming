from collections import deque

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
#move = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
#歩数カウント不要ならvisited = set()として、都度visited.add(nx+ny*C)して管理する方法も可
def bfs(sy,sx,gy,gx):
    queue = deque([[sy,sx]])
    visited = [[False]*W for _ in range(H)]
    visited[sy][sx] = 0
    while queue:
        y,x = queue.popleft()
        if [y,x] == [gy,gx]:
            return visited[y][x]
        for dy,dx in move:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and maze[ny][nx] == "." and visited[ny][nx] == -1:
                visited[ny][nx] = visited[y][x] + 1
                queue.append([ny, nx])

H,W = map(int, input().split())
sy,sx = map(int, input().split())
gy,gx = map(int, input().split())
sy,sx,gy,gx = sy-1,sx-1,gy-1,gx-1

maze = [input() for _ in range(H)]
print(bfs(sy,sx,gy,gx))

from collections import deque

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs_MultiStart(s):
    global cnt_black
    queue = deque(s)

    ans = 0
    while queue:
        if cnt_black == H*W:
            return ans
        ans += 1
        for _ in range(len(queue)):
            y,x = queue.popleft()
            for dy,dx in move:
                ny,nx = y+dy,x+dx
                if 0<=ny<H and 0<=nx<W and A[ny][nx] == ".":
                    A[ny][nx] = "#"
                    cnt_black += 1
                    queue.append((ny, nx))


H,W = map(int,input().split())
A = [list(input()) for _ in range(H)]

start = []
cnt_black = 0
for h in range(H):
    for w in range(W):
        if A[h][w] == "#":
            start.append((h,w))
            cnt_black += 1

ans = bfs_MultiStart(start)
print(ans)