import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())

grid = [[-1]*N for _ in range(N)]
grid[N//2][N//2] = "T"
grid[0][0] = 1
cur = 2
dir = 0
y,x = 0,0
DIR = [(0,1),(1,0),(0,-1),(-1,0)]
while cur < N*N:
    dy,dx = DIR[dir]
    ny,nx = y+dy,x+dx
    if 0<=ny<N and 0<=nx<N and grid[ny][nx] == -1 and grid[ny][nx] != "T":
        grid[ny][nx] = cur
        cur += 1
        y,x = ny,nx
    else:
        dir = (dir+1)%4

for y in range(N):
    print(*grid[y])