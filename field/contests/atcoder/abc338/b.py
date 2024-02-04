import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = list(input())
S.sort()

from collections import Counter
count = Counter(S)

ma = 0
ans = ""
for key in count:
    if count[key] > ma:
        ma = count[key]
        ans = key
print(ans)