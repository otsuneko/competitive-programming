from copy import deepcopy

R,C = map(int,input().split())
B = [list(input()) for _ in range(R)]

ans = deepcopy(B)
for y in range(R):
    for x in range(C):
        if B[y][x] not in [".","#"]:
            bomb = int(B[y][x])
            for dy in range(-bomb,bomb+1):
                for dx in range(-bomb,bomb+1):
                    ny,nx = y+dy,x+dx
                    dist = abs(ny-y) + abs(nx-x)
                    if 0<=ny<R and 0<=nx<C and dist <= bomb:
                        ans[ny][nx] = "."

for y in range(R):
    print("".join(ans[y]))