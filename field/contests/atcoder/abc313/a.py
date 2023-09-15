import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

ans = 0
ma = A[0]

if max(A) == A[0]:
    if A.count(A[0]) == 1:
        print(0)
        exit()
    else:
        print(1)
        exit()

for i in range(1,N):
    if A[i] > ma:
        ma = A[i]
        ans = A[0]-ma-1

print(-ans)