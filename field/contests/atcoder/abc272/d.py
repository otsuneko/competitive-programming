from collections import deque
def bfs():
    queue = deque([[0,0]])
    visited[0][0] = 0
    while queue:
        y,x = queue.popleft()
        for ny in range(N):
            if (ny-y)**2 > M:
                continue
            dx = (M - (ny-y)**2)**0.5
            if int(dx) != dx:
                continue
            nx = int(x+dx)
            if 0 <= nx < N and visited[ny][nx] == -1:
                queue.append((ny,nx))
                visited[ny][nx] = visited[y][x] + 1
            nx = int(x-dx)
            if 0 <= nx < N and visited[ny][nx] == -1:
                queue.append((ny,nx))
                visited[ny][nx] = visited[y][x] + 1

N,M = map(int,input().split())
visited = [[-1]*N for _ in range(N)]
bfs()
for y in range(N):
    print(*visited[y])