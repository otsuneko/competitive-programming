import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,Q = map(int,input().split())
A = list(map(int,input().split()))

rot = 0
for _ in range(Q):
    T,x,y = map(int,input().split())
    x,y = x-1,y-1
    if T == 1:
        A[(x-rot)%N],A[(y-rot)%N] = A[(y-rot)%N],A[(x-rot)%N]
    elif T == 2:
        rot = (rot+1)%N
    elif T == 3:
        print(A[(x-rot)%N])