import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = [list(input()) for _ in range(12)]

ans = 0
for i,s in enumerate(S,1):
    if len(s) == i:
        ans += 1
print(ans)
