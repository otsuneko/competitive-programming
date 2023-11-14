import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W = map(int,input().split())
A = [list(input()) for _ in range(H)]
sy,sx = 0,0
gy,gx = 0,0

DIR = {"^":(-1,0), ">":(0,1), "v":(1,0), "<":(0,-1)}
eye = [[False]*W for _ in range(H)]

for dir in DIR:
    for y in range(H):
        for x in range(W):
            if A[y][x] == "S":
                sy,sx = y,x
            if A[y][x] == "G":
                gy,gx = y,x

            if A[y][x] != dir:
                continue
            ny,nx = y,x
            while 1:
                ny,nx = ny+DIR[dir][0], nx+DIR[dir][1]
                if not (0<=ny<H and 0<=nx<W and A[ny][nx] == "."):
                    break
                eye[ny][nx] = True

from collections import deque
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs(sy,sx,gy,gx):
    queue = deque([[sy,sx]])
    visited = [[-1]*W for _ in range(H)]
    visited[sy][sx] = 0
    while queue:
        y,x = queue.popleft()
        if [y,x] == [gy,gx]:
            return visited[y][x]
        for dy,dx in MOVE:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and A[ny][nx] in [".","G"] and visited[ny][nx] == -1 and eye[ny][nx] == False:
                visited[ny][nx] = visited[y][x] + 1
                queue.append([ny, nx])
    return -1

# print(*A, sep="\n")
print(bfs(sy,sx,gy,gx))

# row = [False]*H
# col = [False]*W

# for y in range(H):
#     for x in range(W):
#         if A[y][x] in [".","!"]:
#             if (row[y] or col[x]):
#                 A[y][x] = "!"
#         elif A[y][x] == ">":
#             row[y] = True
#             col[x] = False
#         elif A[y][x] == "v":
#             col[x] = True
#             row[y] = False
#         elif A[y][x] == "S":
#             sy,sx = y,x
#         elif A[y][x] == "G":
#             gy,gx = y,x
#         else:
#             row[y] = col[x] = False

# row = [False]*H
# col = [False]*W

# for y in range(H-1,-1,-1):
#     for x in range(W-1,-1,-1):
#         if A[y][x] in [".","!"]:
#             if (row[y] or col[x]):
#                 A[y][x] = "!"
#         elif A[y][x] == "<":
#             row[y] = True
#             col[x] = False
#         elif A[y][x] == "^":
#             col[x] = True
#             row[y] = False
#         else:
#             row[y] = col[x] = False

# from collections import deque

# MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
# def bfs(sy,sx,gy,gx):
#     queue = deque([[sy,sx]])
#     visited = [[-1]*W for _ in range(H)]
#     visited[sy][sx] = 0
#     while queue:
#         y,x = queue.popleft()
#         if [y,x] == [gy,gx]:
#             return visited[y][x]
#         for dy,dx in MOVE:
#             ny,nx = y+dy,x+dx
#             if 0<=ny<H and 0<=nx<W and A[ny][nx] in [".","G"] and visited[ny][nx] == -1:
#                 visited[ny][nx] = visited[y][x] + 1
#                 queue.append([ny, nx])
#     return -1

# # print(*A, sep="\n")
# print(bfs(sy,sx,gy,gx))