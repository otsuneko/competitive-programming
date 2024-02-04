import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from collections import deque

MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1],[1,1],[-1,-1])
def bfs(sy,sx):
    queue = deque([[sy,sx]])
    while queue:
        y,x = queue.popleft()
        for dy,dx in MOVE:
            ny,nx = y+dy,x+dx
            if(ny,nx) in pos and (ny,nx) not in seen:
                seen.add((ny,nx))
                queue.append([ny, nx])

N = int(input())
pos = set([tuple(map(int,input().split())) for _ in range(N)])
seen = set()

ans = 0
for x,y in pos:
    if (x,y) in seen:
        continue
    bfs(x,y)
    ans += 1
print(ans)