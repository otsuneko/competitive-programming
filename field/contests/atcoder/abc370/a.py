import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

L,R = map(int,input().split())

if (L+R)%2 == 0:
    print("Invalid")
elif L == 1:
    print("Yes")
else:
    print("No")
