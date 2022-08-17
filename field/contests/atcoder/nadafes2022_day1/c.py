from collections import deque

move = ((1, 0), (-1, 0), (0, 1), (0, -1))
def bfs_lava(lava):
    while lava:
        for _ in range(len(lava)):
            y,x = lava.popleft()
            next = grid[y][x] + K
            for dy,dx in move:
                ny,nx = y+dy,x+dx
                if 0<=ny<H and 0<=nx<W and grid[ny][nx] != "#":
                    if grid[ny][nx] == "." or grid[ny][nx] > next:
                        grid[ny][nx] = next
                        lava.append((ny, nx))

def bfs_game(sy,sx,grid,visited):
    queue = deque([(sy, sx)])
    visited[sy][sx] = True
    count = 0
    while queue and not visited[H-1][W-1]:
        count += 1
        for _ in range(len(queue)):
            y,x = queue.popleft()
            for dy,dx in move:
                ny,nx = y+dy,x+dx
                if 0<=ny<H and 0<=nx<W and not visited[ny][nx] and count < grid[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((ny, nx))

H,W,K =map(int,input().split())
grid = [list(input()) for _ in range(H)]
lava = deque()

for h in range(H):
    for w in range(W):
        if grid[h][w] == "@":
            lava.append((h,w))
            grid[h][w] = 0
        elif grid[h][w] == "#":
            grid[h][w] = 0

bfs_lava(lava)

for h in range(H):
    for w in range(W):
        if grid[h][w] == ".":
            grid[h][w] = 10**18

# print(*grid, sep="\n")
visited = [[False]*W for _ in range(H)]
bfs_game(0,0,grid,visited)
print(["No","Yes"][visited[H-1][W-1]])