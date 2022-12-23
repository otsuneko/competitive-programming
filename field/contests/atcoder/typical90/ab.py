N = int(input())
H=W=1001
A = [[0]*W for _ in range(H)]
for _ in range(N):
    lx,ly,rx,ry = map(int,input().split())
    A[ly][lx] += 1
    A[ry][rx] += 1
    A[ry][lx] -= 1
    A[ly][rx] -= 1

for y in range(H):
    for x in range(1,W):
        A[y][x] += A[y][x-1]

for y in range(1,H):
    for x in range(W):
        A[y][x] += A[y-1][x]

ans = [0]*N
for y in range(H):
    for x in range(W):
        if 0 < A[y][x] <= N:
            ans[A[y][x]-1] += 1
for a in ans:
    print(a)