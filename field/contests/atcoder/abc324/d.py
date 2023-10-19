import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = list(input())

from collections import Counter
count = Counter(S)

ans = 0
for i in range(int((10**N)**0.5)+1):
    p = list(str(i**2))
    p += ["0"]*(N-len(p))
    count2 = Counter(p)

    if count == count2:
        ans += 1
print(ans)