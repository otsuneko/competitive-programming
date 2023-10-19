import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M,P = map(int,input().split())

ans = 0
moon = M
for day in range(1,N+1):
    if day == moon:
        ans += 1
        moon += P
print(ans)