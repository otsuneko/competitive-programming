import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right

N = int(input())
lr = []
li = []
for i in range(N):
    l,r = map(int,input().split())
    lr.append((l,r))
    li.append(l)
lr.sort(key=lambda x:x[0])
li.sort()

ans = 0
for i in range(N):
    l,r = lr[i]
    idx = bisect(li,r)
    ans += idx-i-1
print(ans)
