import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S,T = map(str,input().split())

if S == "AtCoder" and T == "Land":
    print("Yes")
else:
    print("No")
