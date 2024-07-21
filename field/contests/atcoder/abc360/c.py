import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right

N = int(input())
A = list(map(int,input().split()))
W = list(map(int,input().split()))

boxes = [[] for _ in range(N)]

for i in range(N):
    insort(boxes[A[i]-1],W[i])

ans = 0
for box in boxes:
    if len(box) <= 1:
        continue
    ans += sum(box) - box[-1]
print(ans)
