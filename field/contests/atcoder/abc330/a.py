import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

M,D = map(int,input().split())
y,m,d = map(int,input().split())

if d+1 > D:
    d = 1
    m += 1
else:
    d += 1

if m > M:
    m = 1
    y += 1

print(y,m,d)