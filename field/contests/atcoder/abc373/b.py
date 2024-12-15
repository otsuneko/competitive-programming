import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()

alphabet = list("BCDEFGHIJKLMNOPQRSTUVWXYZ")

cur = S.index("A")
ans = 0
for a in alphabet:
    ans += abs(cur - S.index(a))
    cur = S.index(a)
print(ans)
