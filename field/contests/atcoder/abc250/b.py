N,A,B =map(int,input().split())


tile = ""
tile_inv = ""
for i in range(N):
    if i%2 == 0:
        tile += "."*B
        tile_inv += "#"*B
    else:
        tile += "#"*B
        tile_inv += "."*B

cnt = 0
flg = True
for _ in range(N*A):
    if flg:
        print(tile)
    else:
        print(tile_inv)
    cnt += 1
    if cnt == A:
        cnt = 0
        flg = not flg