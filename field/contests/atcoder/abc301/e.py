from collections import deque

MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs(sy,sx):
    queue = deque([[sy,sx]])
    visited = [[INF]*W for _ in range(H)]
    visited[sy][sx] = 0
    while queue:
        y,x = queue.popleft()
        for dy,dx in MOVE:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and A[ny][nx] != "#" and visited[ny][nx] == INF:
                visited[ny][nx] = visited[y][x] + 1
                queue.append([ny, nx])
    return visited

import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W,T = map(int,input().split())
A = [list(input()) for _ in range(H)]

# S,お菓子,G間の距離を算出
sy,sx,gy,gx = 0,0,0,0
okashi = []
for y in range(H):
    for x in range(W):
        if A[y][x] == "S":
            sy,sx = y,x
        elif A[y][x] == "G":
            gy,gx = y,x
        elif A[y][x] == "o":
            okashi.append((y,x))

N = len(okashi)

# dists[i]は、i 個目のお菓子マスを始点とする距離テーブル
dists = [[[INF]*W for _ in range(H)] for _ in range(N)]
for i in range(N):
    y,x = okashi[i]
    dists[i] = bfs(y,x)

# print(*dists, sep="\n")

# bitDP
dp = [[INF]*N for _ in range(1<<N)]

for i in range(N):
    dp[1<<i][i] = dists[i][sy][sx]

# print(*dp, sep="\n")

for S in range(1,1<<N):
    for last in range(N):
        if dp[S][last] == INF:
            continue
        for nxt in range(N):
            # まだnxtに訪れていない場合
            if S & (1 << nxt) == 0:
                dp[S|(1<<nxt)][nxt] = min(dp[S|(1<<nxt)][nxt], dp[S][last] + dists[last][okashi[nxt][0]][okashi[nxt][1]])

# print(*dp, sep="\n")

ans = -1
if bfs(sy,sx)[gy][gx] <= T:
    ans = 0

for S in range(1,1<<N):
    for last in range(N):
        if dp[S][last] + dists[last][gy][gx] <= T:
            cnt = 0
            for i in range(N):
                if S & (1 << i):
                    cnt += 1
            ans = max(ans,cnt)
print(ans)