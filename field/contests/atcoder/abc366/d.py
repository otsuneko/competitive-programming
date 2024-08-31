import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = [[list(map(int,input().split())) for _ in range(N)] for _ in range(N)]

cumsum = [[[0]*(N+1) for _ in range(N+1)] for _ in range(N)]

for z in range(N):
    for y in range(N):
        for x in range(N):
            cumsum[z][y+1][x+1] = cumsum[z][y][x+1] + cumsum[z][y+1][x] - cumsum[z][y][x] + A[z][y][x]

Q = int(input())
for _ in range(Q):
    z1,z2,y1,y2,x1,x2 = map(int,input().split())
    x1 -= 1
    y1 -= 1
    z1 -= 1
    ans = 0
    for z in range(z1,z2):
        ans += cumsum[z][y2][x2] - cumsum[z][y2][x1] - cumsum[z][y1][x2] + cumsum[z][y1][x1]
    print(ans)
