import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int, input().split()))

diff = []
for i in range(N-1):
    diff.append(A[i+1]-A[i])

from itertools import groupby
rle = [(k, len(list(g))) for k,g in groupby(diff)]

ans = N
for _,cnt in rle:
    ans += (cnt+1)*cnt//2
print(ans)
