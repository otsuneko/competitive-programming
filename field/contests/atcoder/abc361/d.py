import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import copy

N = int(input())
S = list(input()) + [".", "."]
T = input() + ".."

dp = set(["".join(S)])
from collections import defaultdict
memo = defaultdict(int)
memo["".join(S)] = 0

while dp:
    dp2 = set()
    for s in dp:
        s2 = list(s)
        blank_idx = s2.index(".")

        for i in range(N+1):
            if not (s2[i] != "." and s2[i+1] != "."):
                continue
            idx1,idx2 = i,i+1
            s2[idx1],s2[blank_idx] = s2[blank_idx],s2[idx1]
            s2[idx2],s2[blank_idx+1] = s2[blank_idx+1],s2[idx2]
            if "".join(s2) not in memo:
                dp2.add("".join(s2))
                memo["".join(s2)] = memo[s] + 1
            s2[idx1],s2[blank_idx] = s2[blank_idx],s2[idx1]
            s2[idx2],s2[blank_idx+1] = s2[blank_idx+1],s2[idx2]
    dp = copy.deepcopy(dp2)

if T in memo:
    print(memo[T])
else:
    print(-1)
