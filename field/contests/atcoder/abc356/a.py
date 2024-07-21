import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,L,R = map(int,input().split())

A = [i+1 for i in range(N)]
A = A[:L-1] + A[L-1:R][::-1] + A[R:]

print(*A)
