import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
A = list(map(int,input().split()))
A.sort()

ans = INF
for i in range(K+1):
    ans = min(ans, A[i+(N-K-1)] - A[i])
print(ans)
