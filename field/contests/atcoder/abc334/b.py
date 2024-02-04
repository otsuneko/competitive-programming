import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

A,M,L,R = map(int,input().split())

L -= A
R -= A
A = 0

ans = -(-(R-L)//M)
print(ans)