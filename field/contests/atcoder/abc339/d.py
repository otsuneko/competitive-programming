import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = [list(input()) for _ in range(N)]

from collections import deque

MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs(sy1,sx1,sy2,sx2):
    queue = deque([[sy1,sx1,sy2,sx2]])
    dist = [[[[INF]*N for _ in range(N)] for _ in range(N)] for _ in range(N)]
    dist[sy1][sx1][sy2][sx2] = 0
    while queue:
        y1,x1,y2,x2 = queue.popleft()
        if [y1,x1] == [y2,x2]:
            print(dist[y1][x1][y2][x2])
            exit()
        for dy, dx in MOVE:
            ny1,nx1 = y1+dy,x1+dx
            ny2,nx2 = y2+dy,x2+dx
            if not(0 <= ny1 < N and 0 <= nx1 < N and S[ny1][nx1] != "#"):
                ny1,nx1 = y1,x1
            if not(0 <= ny2 < N and 0 <= nx2 < N and S[ny2][nx2] != "#"):
                ny2,nx2 = y2,x2
            if dist[ny1][nx1][ny2][nx2] == INF:
                dist[ny1][nx1][ny2][nx2] = dist[y1][x1][y2][x2] + 1
                queue.append([ny1,nx1,ny2,nx2])

s = []
for y in range(N):
    for x in range(N):
        if S[y][x] == "P":
            s.append((y,x))

bfs(*s[0],*s[1])
print(-1)