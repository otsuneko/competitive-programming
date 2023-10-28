import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from collections import deque

# MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
MOVE = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
#歩数カウント不要ならvisited = set()として、都度visited.add(nx+ny*C)して管理する方法も可
def bfs(sy,sx):
    queue = deque([[sy,sx]])
    visited[sy][sx] = 0
    while queue:
        y,x = queue.popleft()
        visited[y][x] = 1
        for dy,dx in MOVE:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and S[ny][nx] == "#" and visited[ny][nx] == -1:
                visited[ny][nx] = visited[y][x] + 1
                queue.append([ny, nx])

H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]

visited = [[-1]*W for _ in range(H)]
ans = 0
for y in range(H):
    for x in range(W):
        if visited[y][x] != -1 or S[y][x] != "#":
            continue
        bfs(y,x)
        ans += 1
print(ans)