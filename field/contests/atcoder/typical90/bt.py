# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)
move = ([1, 0], [-1, 0], [0, 1], [0, -1])
def dfs(y,x,sy,sx,cnt):

    if [y,x] == [sy,sx] and cnt >= 4:
        return cnt

    ret = 0
    for dy, dx in move:
        ny,nx = y+dy,x+dx
        if 0 <= ny < H and 0 <= nx < W and C[ny][nx] == "." and seen[ny][nx] == False:
            seen[ny][nx] = True
            ret = max(ret, dfs(ny,nx,sy,sx,cnt+1))
            seen[ny][nx] = False
    
    return ret

H,W = map(int,input().split())
C =[list(input()) for _ in range(H)]

ans = 0
for y in range(H):
    for x in range(W):
        seen = [[False]*W for _ in range(H)]
        ans = max(ans, dfs(y,x,y,x,0))

if ans < 4:
    print(-1)
else:
    print(ans)