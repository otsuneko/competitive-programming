import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N =  int(input())
A =  [list(input()) for _ in range(N)]
B = [list(input()) for _ in range(N)]

for y in range(N):
    for x in range(N):
        if A[y][x] != B[y][x]:
            print(y+1,x+1)
            exit()
