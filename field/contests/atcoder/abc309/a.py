import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

A,B = map(int,input().split())

if B-A == 1 and B not in [1,4,7]:
    print("Yes")
else:
    print("No")