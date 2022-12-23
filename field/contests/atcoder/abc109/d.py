from collections import deque

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs(h,w):
    queue = deque([(h,w,[])])
    while queue:
        y,x,mv = queue.popleft()
        if A[y][x]%2 and [y,x] != [h,w]:
            return mv
        for dy,dx in move:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and seen[ny][nx] == False and [ny,nx] not in mv:
                nmv = mv[:]
                nmv.append([ny,nx])
                queue.append((ny,nx,nmv))

H,W = map(int,input().split())
A = []
cnt_odd = 0
for _ in range(H):
    row = list(map(int,input().split()))
    for r in row:
        if r%2:
            cnt_odd += 1
    A.append(row)

ans = []
seen =[[False]*W for _ in range(H)]
for h in range(H):
    for w in range(W):
        if cnt_odd%2:
            if cnt_odd == 1:
                break
        else:
            if cnt_odd == 0:
                break
        if A[h][w]%2:
            seen[h][w] = True
            mv = bfs(h,w)
            py,px = h,w
            if not mv:
                continue
            for i in range(len(mv)):
                y,x = mv[i]
                A[py][px] -= 1
                A[y][x] += 1
                ans.append((py+1,px+1,y+1,x+1))
                py,px = y,x
                seen[y][x] = True
            cnt_odd -= 2

# print(*A, sep="\n")
print(len(ans))
for a in ans:
    print(*a)