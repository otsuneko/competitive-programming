import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from collections import deque

MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs_MultiStart(pos,s):
    queue = deque(s)

    ans = set(pos)
    while queue:
        for _ in range(len(queue)):
            y,x,d = queue.popleft()
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if 0<=ny<H and 0<=nx<W and S[ny][nx] == "." and d+1 <= D:
                    S[ny][nx] = "H"
                    ans.add((ny,nx))
                    queue.append((ny, nx, d+1))
    return len(ans)

H,W,D = map(int,input().split())
S = [list(input()) for _ in range(H)]

pos = []
humid = []
for y in range(H):
    for x in range(W):
        if S[y][x] == "H":
            pos.append((y,x))
            humid.append((y,x,0))

ans = bfs_MultiStart(pos,humid)
print(ans)
