import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

sys.setrecursionlimit(10**7)

MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1]) #縦横移動
def dfs(y,x,path):
    global ans

    if len(path) == K+1:
        ans += 1
        return

    for dy,dx in MOVE:
        ny,nx = y+dy,x+dx
        if 0 <= ny < H and 0 <= nx < W and grid[ny][nx] == "." and (ny,nx) not in path:
            path.add((ny,nx))
            dfs(ny,nx,path)
            path.remove((ny,nx))

H,W,K = map(int, input().split())
grid = [input() for _ in range(H)]

ans = 0
for y in range(H):
    for x in range(W):
        if grid[y][x] == ".":
            dfs(y,x,set([(y,x)]))
print(ans)
