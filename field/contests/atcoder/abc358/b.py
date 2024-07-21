import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,A = map(int,input().split())
T = list(map(int,input().split()))

cur = 0
for i in range(N):
    if T[i] > cur:
        cur = T[i]+A
    else:
        cur += A
    print(cur)
