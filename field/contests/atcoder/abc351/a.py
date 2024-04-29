import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

A =  list(map(int,input().split()))
B =  list(map(int,input().split()))

print(sum(A)-sum(B)+1)
