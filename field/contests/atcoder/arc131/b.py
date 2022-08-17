H,W = map(int,input().split())
C = [list(input()) for _ in range(H)]

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
for y in range(H):
    for x in range(W):
        if C[y][x] == ".":
            check = [1,2,3,4,5]
            for dy,dx in move:
                ny,nx = y+dy,x+dx
                if 0 <= ny < H and 0 <= nx < W and C[ny][nx] != "." and int(C[ny][nx]) in check:
                    check.remove(int(C[ny][nx]))
            C[y][x] = str(check[0])

for c in C:
    print("".join(c))