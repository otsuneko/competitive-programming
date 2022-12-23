N = int(input())
D = [list(map(int,input().split())) for _ in range(N)]
Q = int(input())
P = [int(input()) for _ in range(Q)]

cumsum = [[0]*(N+1) for _ in range(N+1)]
for y in range(N):
    for x in range(N):
        cumsum[y+1][x+1] = cumsum[y][x+1] + cumsum[y+1][x] - cumsum[y][x] + D[y][x]

for p in P:
    ma = 0
    for y1 in range(N):
        for x1 in range(N):
            for y2 in range(y1+1,N+1):
                for x2 in range(x1+1,N+1):
                    if (y2-y1) * (x2-x1) > p:
                        break
                    ma = max(ma, cumsum[y2][x2] - cumsum[y2][x1] - cumsum[y1][x2] + cumsum[y1][x1])
    print(ma)
