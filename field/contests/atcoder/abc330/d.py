import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18


N,Q = map(int,input().split())
P = [list(input()) for _ in range(N)]
A = [[0]*N for _ in range(N)]
for y in range(N):
    for x in range(N):
        if P[y][x] == "B":
            A[y][x] = 1


y2,x2,y1,x1 = N,N,1,1

cumsum = [[0]*(N+1) for _ in range(N+1)]
for y in range(N):
    for x in range(N):
        cumsum[y+1][x+1] = cumsum[y][x+1] + cumsum[y+1][x] - cumsum[y][x] + A[y][x]

# print(*cumsum,sep="\n")
# print(cumsum[y2][x2] - cumsum[y2][x1-1] - cumsum[y1-1][x2] + cumsum[y1-1][x1-1])

for _ in range(Q):
    a,b,c,d = map(int,input().split())
    diff_y = c//N - a//N
    diff_x = d//N - b//N

    if diff_y > 0 and diff_x > 0:
        
