import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

# 二次元配列の90度右回転
def rotate_2d(arr):
    return list(zip(*arr[::-1]))

P = [list(input()) for _ in range(12)]

#1個目の連結成分
flg = False
p1 = [(0,0)]
for y in range(4):
    for x in range(4):
        if not flg and P[y][x] == "#":
            flg = True
            by,bx = y,x
        elif flg and P[y][x] == "#":
            p1.append((y-by,x-bx))

#2個目の連結成分
P2 = [[""]*4 for _ in range(4)]
for y in range(4):
    for x in range(4):
        P2[y][x] = P[y+4][x]
p2 = []
for i in range(4):
    tmp = [(0,0)]
    flg = False
    for y in range(4):
        for x in range(4):
            if not flg and P2[y][x] == "#":
                flg = True
                by,bx = y,x
            elif flg and P2[y][x] == "#":
                tmp.append((y-by,x-bx))
    p2.append(tmp)
    P2 = rotate_2d(P2)

#3個目の連結成分
P3 = [[""]*4 for _ in range(4)]
for y in range(4):
    for x in range(4):
        P3[y][x] = P[y+8][x]
p3 = []
for i in range(4):
    tmp = [(0,0)]
    flg = False
    for y in range(4):
        for x in range(4):
            if not flg and P3[y][x] == "#":
                flg = True
                by,bx = y,x
            elif flg and P3[y][x] == "#":
                tmp.append((y-by,x-bx))
    p3.append(tmp)
    P3 = rotate_2d(P3)

for y in range(4):
    for x in range(4):
        flg = False
        grid = [["."]*4 for _ in range(4)]
        
        for dy,dx in p1:
            ny,nx = y+dy,x+dx
            if not (0<=ny<4 and 0<=nx<4):
                flg = True
                break
            grid[ny][nx] = "#"

        if flg:
            continue

        # 2個目の場所と向き
        for rot in range(4):
            for y2 in range(4):
                for x2 in range(4):
                    if grid[y2][x2] != ".":
                        continue
                    grid2 = [a[:] for a in grid]
                    for dy,dx in p2[rot]:
                        ny,nx = y2+dy,x2+dx
                        if not (0<=ny<4 and 0<=nx<4 and grid2[ny][nx] == "."):
                            break
                        grid2[ny][nx] = "#"

                    else:
                        # 3個目の場所と向き
                        for rot2 in range(4):
                            for y3 in range(4):
                                for x3 in range(4):
                                    if grid2[y3][x3] != ".":
                                        continue
                                    grid3 = [a[:] for a in grid2]
                                    for dy,dx in p3[rot2]:
                                        ny,nx = y3+dy,x3+dx
                                        if not (0<=ny<4 and 0<=nx<4 and grid3[ny][nx] == "."):
                                            break
                                        grid3[ny][nx] = "#"
                                    else:
                                        # 検算
                                        for y4 in range(4):
                                            if grid3[y4].count("#") != 4:
                                                break
                                        else:
                                            print("Yes")
                                            exit()
print("No")