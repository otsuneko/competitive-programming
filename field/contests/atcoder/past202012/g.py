import sys
import random
sys.setrecursionlimit(10**7)
def rand_ints_nodup(a, b, k):
  ns = []
  while len(ns) < k:
    n = random.randint(a, b)
    if not n in ns:
      ns.append(n)
  return ns

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
def dfs(x,y,n,path):
    global k
    global max_path
    global seen
    seen[y][x] = True
    cnt = 0
    rand_idx = rand_ints_nodup(0,3,4)
    for i in rand_idx:
        nx = x + dx[i]
        ny = y + dy[i]
        if 0 <= nx < W and 0 <= ny < H and seen[ny][nx] == False and S[ny][nx] == "#":
            path.append((ny+1,nx+1))
            dfs(nx,ny,n+1,path)
        else:
            cnt += 1
    if cnt == 4:
        if n > k:
            k = n
            max_path = path
        return

H, W = map(int,input().split())
S = [list(input()) for _ in range(H)]

k = 0
max_path = []
for y in range(H):
    for x in range(W):
        if S[y][x] == "#":
            for _ in range(100):
                seen = [[False]*W for i in range(H)]
                seen[y][x] = True
                path = [(y+1,x+1)]
                dfs(x,y,1,path)

print(k)
for p in max_path:
    print(*p)