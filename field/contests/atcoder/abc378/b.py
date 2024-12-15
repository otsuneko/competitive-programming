import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
gomi = [list(map(int,input().split())) for _ in range(N)]

Q = int(input())
for _ in range(Q):
    t,d = map(int,input().split())
    t -= 1

    q,r = gomi[t]

    p = d//q
    if p*q+r < d:
        print(p*q+r+q)
    else:
        print(p*q+r)
