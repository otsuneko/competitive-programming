from collections import deque

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs(sy,sx, color):
    queue = deque([[sy, sx]])
    s = set([(sy,sx)])
    while queue:
        y,x = queue.popleft()
        for dy,dx in move:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and B[ny][nx] == color and visited[ny][nx] == False:
                visited[ny][nx] = True
                queue.append([ny, nx])
                s.add((ny,nx))    
    return s

H,W,N =map(int,input().split())
A =[list(map(int,input().split())) for _ in range(H)]
C =list(map(int,input().split()))

B = [[0]*W for _ in range(H)]
province = [set() for _ in range(N)]
for h in range(H):
    for w in range(W):
        B[h][w] = C[A[h][w]-1]
        province[A[h][w]-1].add((h,w))

visited = [[False]*W for _ in range(H)]
colors = [set() for _ in range(N)]
for h in range(H):
    for w in range(W):
        if not visited[h][w]:
            visited[h][w] = True
            area = bfs(h,w,B[h][w])
            colors[A[h][w]-1] |= area

for i in range(N):
    if province[i] != colors[i]:
        print("No")
        break
else:
    print("Yes")