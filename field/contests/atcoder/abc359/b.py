import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

ans = 0
for i in range(N):
    for j in range(2*N-2):
        if A[j] == i+1 and A[j] == A[j+2]:
            ans += 1
print(ans)
