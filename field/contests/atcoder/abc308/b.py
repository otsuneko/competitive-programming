import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
C = list(map(str,input().split()))
D = list(map(str,input().split()))
P = list(map(int,input().split()))

ans = 0
for i in range(N):
    if C[i] in D:
        idx = D.index(C[i])
    else:
        ans += P[0]
        continue
    ans += P[idx+1]
print(ans)