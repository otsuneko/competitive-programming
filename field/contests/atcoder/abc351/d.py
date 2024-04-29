import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W =  map(int,input().split())
S =  [list(input()) for _ in range(H)]

from collections import deque

MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs(sy,sx):
    queue = deque([[sy,sx]])
    visited[sy][sx] = 0
    seen = set([(sy,sx)])
    res = 1
    while queue:
        y,x = queue.popleft()
        for dy,dx in MOVE:
            ny,nx = y+dy,x+dx
            if not (0<=ny<H and 0<=nx<W):
                continue
            if S[ny][nx] == ".":
                if visited[ny][nx] == -1:
                    visited[ny][nx] = visited[y][x] + 1
                    queue.append([ny, nx])
                    res += 1
            elif S[ny][nx] == "M" and (ny,nx) not in seen:
                seen.add((ny,nx))
                res += 1
    return res

for y in range(H):
    for x in range(W):
        if S[y][x] == "#":
            continue
        for dy,dx in MOVE:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and S[ny][nx] == "#":
                S[y][x] = "M"
                break

ans = 1
visited = [[-1]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if S[y][x] != "." or visited[y][x] != -1:
            continue
        ans = max(ans, bfs(y,x))
print(ans)
