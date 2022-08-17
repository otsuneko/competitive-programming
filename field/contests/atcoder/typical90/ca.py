H,W = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]
B = [list(map(int,input().split())) for _ in range(H)]

ans = 0
for y in range(H-1):
    for x in range(W-1):
        diff = B[y][x] - A[y][x]
        ans += abs(diff)
        for y2 in range(y,y+2):
            for x2 in range(x,x+2):
                A[y2][x2] += diff

if A == B:
    print("Yes")
    print(ans)
else:
    print("No")