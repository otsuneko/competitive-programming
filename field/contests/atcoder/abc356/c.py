import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M,K = map(int,input().split())
C = []
A = []
R = []
for _ in range(M):
    c,*a,r = map(str,input().split())
    C.append(int(c))
    A.append([int(i) for i in a])
    R.append(r)

import itertools

ans = 0
for bit in itertools.product([True, False], repeat=N):

    for i,a in enumerate(A):
        keys = 0
        for n in a:
            keys += 1 if bit[n-1] else 0
        if (keys >= K and R[i] != "o") or (keys < K and R[i] != "x"):
            break
    else:
        ans += 1
print(ans)
