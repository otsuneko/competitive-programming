import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
A = list(map(int,input().split()))

print(*A[-K:] + A[:-K])
