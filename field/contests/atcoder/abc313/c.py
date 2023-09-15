import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))
A.sort()
mean = sum(A)//N
remain = sum(A)-mean*N

B = [mean]*N
# 端数分の調整
for i in range(remain):
    B[N-1-i] += 1

ans = 0
for i in range(N):
    ans += abs(B[i]-A[i])

print(ans//2)