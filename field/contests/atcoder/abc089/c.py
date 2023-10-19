import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = [list(input()) for _ in range(N)]

from collections import defaultdict
dict = defaultdict(int)

for s in S:
    dict[s[0]] += 1

march = "MARCH"

import itertools

ans = 0
for cmb in itertools.combinations(march,3):
    add = 1
    for s in cmb:
        add *= dict[s]
    ans += add
print(ans)