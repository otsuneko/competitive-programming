import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())

ans = N
for _ in range(K):
    s = list(str(ans))
    g1 = int("".join(sorted(s,reverse=True)))
    g2 = int("".join(sorted(s)))
    ans = g1 - g2
print(ans)
