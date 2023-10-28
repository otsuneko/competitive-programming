import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

X,Y = map(int,input().split())
if (X > Y and X-Y > 3) or (X < Y and Y-X > 2):
    print("No")
else:
    print("Yes")