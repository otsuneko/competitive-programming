import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from collections import deque

snuke = ["s","n","u","k","e"]
move = ([1, 0], [-1, 0], [0, 1], [0, -1])
#move = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
#歩数カウント不要ならvisited = set()として、都度visited.add(nx+ny*C)して管理する方法も可
def bfs(sy,sx,gy,gx):
    queue = deque([[sy,sx,0]])
    visited = [[-1]*W for _ in range(H)]
    visited[sy][sx] = 0
    while queue:
        y,x,idx = queue.popleft()
        if [y,x] == [gy,gx]:
            return True
        for dy,dx in move:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and maze[ny][nx] == snuke[(idx+1)%5] and visited[ny][nx] == -1:
                visited[ny][nx] = visited[y][x] + 1
                queue.append([ny, nx, idx+1])

    return False

H,W = map(int, input().split())
sy,sx = [0,0]
gy,gx = [H-1,W-1]

maze = [input() for _ in range(H)]
if maze[0][0] != "s":
    print("No")
    exit()

print("Yes" if bfs(sy,sx,gy,gx) else "No")


