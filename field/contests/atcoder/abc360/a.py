import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

if S.index("R") < S.index("M"):
    print("Yes")
else:
    print("No")
