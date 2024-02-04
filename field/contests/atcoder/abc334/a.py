import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

B,G = map(int,input().split())

if B > G:
    print("Bat")
else:
    print("Glove")