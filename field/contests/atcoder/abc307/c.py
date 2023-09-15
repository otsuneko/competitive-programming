import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

HA,WA = map(int,input().split())
A = [list(input()) for _ in range(HA)]
HB,WB = map(int,input().split())
B = [list(input()) for _ in range(HB)]
HX,WX = map(int,input().split())
X = [list(input()) for _ in range(HX)]

seen = set()
for y in range(HX):
    for x in range(WX):
        if X[y][x] == "#":
            seen.add((y,x))

alist = []
flg = False
basey,basex = 0,0
for y in range(HA):
    for x in range(WA):
        if not flg and A[y][x] == "#":
            basey,basex = y,x
            flg = True
        elif A[y][x] == "#":
            alist.append((y-basey,x-basex))

blist = []
flg = False
basey,basex = 0,0
for y in range(HB):
    for x in range(WB):
        if not flg and B[y][x] == "#":
            basey,basex = y,x
            flg = True
        elif B[y][x] == "#":
            blist.append((y-basey,x-basex))

for ya in range(HX):
    for xa in range(WX):
        if X[ya][xa] != "#":
            continue
        check = set()
        check.add((ya,xa))
        cnt = 0
        for ya2,xa2 in alist:
            ny,nx = ya+ya2,xa+xa2
            if 0<=ny<HX and 0<=nx<WX and X[ny][nx] == "#":
                check.add((ny,nx))
                cnt += 1
        if cnt != len(alist):
            continue

        for yb in range(HX):
            for xb in range(WX):
                    if X[yb][xb] != "#":
                        continue
                    check.add((yb,xb))
                    cnt = 0
                    for yb2,xb2 in blist:
                        ny,nx = yb+yb2,xb+xb2
                        if 0<=ny<HX and 0<=nx<WX and X[ny][nx] == "#":
                            check.add((ny,nx))
                            cnt += 1
                    if cnt != len(blist):
                        continue
                    # print(check,"a",seen)
                    if check == seen:
                        print("Yes")
                        exit()
print("No")