import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = input()

if "ABC" in S:
    print(S.index("ABC")+1)
else:
    print(-1)