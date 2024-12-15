import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = list(input())
N.sort()
N = "".join(N)

if N == "122333":
    print("Yes")
else:
    print("No")
