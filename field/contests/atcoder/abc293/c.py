# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

move = ([1, 0], [0, 1])
def dfs(y,x,path):
    global ans
    if (y,x) == (H-1,W-1):
        if len(path) == len(set(path)):
            ans += 1

    for dy, dx in move:
        ny,nx = y+dy,x+dx
        if 0 <= ny < H and 0 <= nx < W:
            path.append(A[ny][nx])
            dfs(ny,nx,path)
            path.pop()

H,W = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]
ans = 0

dfs(0,0,[A[0][0]])
print(ans)