import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
S = input()

import more_itertools

ans = 0
seen = set()
for s in more_itertools.distinct_permutations(S):
    for i in range(N-K+1):
        if s[i:i+K] == s[i:i+K][::-1]:
            break
    else:
        ans += 1
print(ans)
