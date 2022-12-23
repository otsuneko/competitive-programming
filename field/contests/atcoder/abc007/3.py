from collections import deque

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
#move = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
#歩数カウント不要ならvisited = set([])として、都度visited.add(nx+ny*C)して管理する方法も可
def bfs(sy, sx, gy, gx):
    queue = deque([[sy, sx]])
    visited = [[-1]*C for _ in range(R)]
    visited[sy][sx] = 0
    while queue:
        y, x = queue.popleft()
        if [y, x] == [gy, gx]:
            return visited[y][x]
        for dy,dx in move:
            ny,nx = y+dy,x+dx
            if maze[ny][nx] == "." and visited[ny][nx] == -1:
                visited[ny][nx] = visited[y][x] + 1
                queue.append([ny, nx])

R, C = map(int, input().split())
sy, sx = map(int, input().split())
gy, gx = map(int, input().split())
sy, sx, gy, gx = sy-1, sx-1, gy-1, gx-1

maze = [input() for _ in range(R)]
print(bfs(sy, sx, gy, gx))