import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import itertools

N,M = map(int,input().split())
shops = [list(input()) for _ in range(N)]

ans = INF
for bit in itertools.product([True, False], repeat=N):
    popcorns = [False]*M
    for i,b in enumerate(bit):
        if not b:
            continue
        for j in range(M):
            if shops[i][j] == "o":
                popcorns[j] = True

    if all(popcorns):
        ans = min(ans, bit.count(True))
print(ans)
