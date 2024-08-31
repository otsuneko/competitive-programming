import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

A2 = sorted(A)
print(A.index(A2[-2])+1)
