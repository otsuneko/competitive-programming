import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]

from collections import deque

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs(sy,sx):
    queue = deque([[sy,sx]])
    visited[sy][sx] = 1
    while queue:
        # print(*visited, sep="\n")
        y,x = queue.popleft()
        for dy,dx in move:
            ny,nx = y+dy,x+dx
            while 1:
                if 0<=ny<N and 0<=nx<M and S[ny][nx] == ".":
                    visited[ny][nx] = max(visited[ny][nx],0)
                else:
                    break
                ny,nx = ny+dy,nx+dx

            ny,nx = ny-dy,nx-dx
            if 1<=ny<N-1 and 1<=nx<M-1 and visited[ny][nx] != 1:
                visited[ny][nx] = 1
                queue.append([ny, nx])

sy,sx = [1,1]
visited = [[-1]*M for _ in range(N)]
bfs(sy,sx)
# print(*visited, sep="\n")
ans = 0
for i in range(N):
    for j in range(M):
        if visited[i][j] >= 0:
            ans += 1
print(ans)