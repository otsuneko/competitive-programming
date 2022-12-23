# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)
move = ([1, 0], [0, 1])
def dfs(x, y, path):

    if [x,y] == [W-1, H-1]:
        if (-1,0) not in path and (0,-1) not in path and len(seen) == num_passed:
            print("Possible")
            exit()

    for dy, dx in move:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < W and 0 <= ny < H and (ny,nx) not in seen and A[ny][nx] == "#":
            seen.add((ny,nx))
            path.add((dy,dx))
            dfs(nx, ny, path)
            if (dy,dx) in path:
                path.remove((dy,dx))
            seen.remove((ny,nx))

H,W = map(int,input().split())
A = []
num_passed = 0
for _ in range(H):
    tmp = input()
    A.append(tmp)
    num_passed += tmp.count("#")

path = set()
seen = set((0,0))
dfs(0,0, path)
print("Impossible")