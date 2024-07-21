import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
A = list(map(int,input().split()))

ans = 0
cur = 0
for a in A:
    if cur+a <= K:
        cur += a
    else:
        ans += 1
        cur = a
if cur > 0:
    ans += 1
print(ans)
