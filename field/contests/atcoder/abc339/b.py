import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W,N = map(int,input().split())
grid = [["."]*W for _ in range(H)]

cy,cx = 0,0
dir = "U"
DIR = {"U":(0,1), "R":(1,0), "D":(0,-1), "L":(-1,0)}
DIR2 = {"U":"R", "R":"D", "D":"L", "L":"U"}
DIR3 = {"U":"L", "R":"U", "D":"R", "L":"D"}

for i in range(N):
    if grid[cy][cx] == ".":
        grid[cy][cx] = "#"
        cy,cx = (cy+DIR[dir][0])%H, (cx+DIR[dir][1])%W
        dir = DIR2[dir]
    else:
        grid[cy][cx] = "."
        cy,cx = (cy-DIR[dir][0])%H, (cx-DIR[dir][1])%W
        dir = DIR3[dir]

for i in range(H):
    print("".join(grid[i]))