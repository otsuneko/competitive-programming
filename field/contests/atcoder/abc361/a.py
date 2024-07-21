import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K,X = map(int,input().split())
A = list(map(int,input().split()))

A.insert(K,X)
print(*A)
