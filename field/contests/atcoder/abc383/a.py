import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
humid = [list(map(int,input().split())) for _ in range(N)]

cur = 0
ans = 0
for t,v in humid:
    ans = max(0,ans-(t-cur))
    ans += v
    cur = t

print(ans)
