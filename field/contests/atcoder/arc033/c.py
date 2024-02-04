import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18


Q = int(input())
for _ in range(Q):
    t,x = map(int,input().split())
    if t == 1:
