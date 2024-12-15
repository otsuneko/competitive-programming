import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())
S = input()

from itertools import groupby
rle = [(k, len(list(g))) for k,g in groupby(S)]


idx1 = 0
idx2 = 0

cnt = 0
for i,(s,n) in enumerate(rle):
    if s == "1":
        cnt += 1
        if cnt == K-1:
            idx1 = i
        elif cnt == K:
            idx2 = i

ans = []
for i,(s,n) in enumerate(rle):
    if i == idx1:
        ans += [s]*n
        s2,n2 = rle[idx2]
        ans += [s2]*n2
    elif i == idx2:
        continue
    else:
        ans += [s]*n
print("".join(ans))
