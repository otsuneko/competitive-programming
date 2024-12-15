import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

s = set()

A = list(map(int,input().split()))

ans = 0
for a in A:
    if a in s:
        ans += 1
        s.remove(a)
    else:
        s.add(a)
print(ans)
