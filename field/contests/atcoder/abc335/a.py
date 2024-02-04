import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = list(input())
S[-1] = "4"
print("".join(S))