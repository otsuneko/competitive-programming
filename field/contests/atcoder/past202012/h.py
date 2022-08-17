import sys
sys.setrecursionlimit(10**7)

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
def dfs(y,x):
    if [y,x] == [r-1,c-1] or ans[y][x] == "o":
        for v in visited:
            x = v%W
            y = v//W
            ans[y][x] = "o"
            ok.add(x+y*W)
        return
    for dy, dx in move:
        if S[y][x] == "^":
            if [dy,dx] != [-1,0]:
                continue
        elif S[y][x] == ">":
            if [dy,dx] != [0,1]:
                continue
        elif S[y][x] == "v":
            if [dy,dx] != [1,0]:
                continue
        elif S[y][x] == "<":
            if [dy,dx] != [0,-1]:
                continue
        new_y, new_x = y+dy, x+dx
        if 0 <= new_y < H and 0 <= new_x < W and S[new_y][new_x] != "#" and new_x+new_y*W not in visited:
            visited.add(new_x + new_y*W)

            dfs(new_y,new_x)
            # visited.discard(new_x + new_y*W)

H,W = map(int,input().split())
r,c = map(int,input().split())
S = [list(input()) for _ in range(H)]

ans = [["x"]*W for i in range(H)]
ans[r-1][c-1] = "o"
ok = set([])
for y in range(H):
    for x in range(W):
        visited = set([])
        if S[y][x] != "#":
            if ans[y][x] != "o":
                dfs(y,x)
        else:
            ans[y][x] = "#"
        # print(*ans, sep="\n")

for y in range(H):
    print("".join(ans[y]))