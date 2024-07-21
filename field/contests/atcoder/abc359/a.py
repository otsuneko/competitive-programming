import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = [input() for _ in range(N)]

ans = 0
for s in S:
    if s == "Takahashi":
        ans += 1
print(ans)
