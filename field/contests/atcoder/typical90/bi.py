from collections import deque
import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

Q = int(input())
d = deque()
for _ in range(Q):
    t,x = map(int,input().split())
    if t == 1:
        d.appendleft(x)
    elif t == 2:
        d.append(x)
    else:
        print(d[x-1])