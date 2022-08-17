import sys
input = lambda: sys.stdin.readline().rstrip()

import bisect
import heapq  # heapqライブラリのimport
from collections import deque
Q = int(input())

A = deque()
cnt = 0
for _ in range(Q):
    query = list(map(int,input().split()))

    if query[0] == 1:
        A.append(query[1])
        cnt += 1
    elif query[0] == 2:
        print(A.popleft())
        cnt -= 1
    else:
        A2 = deque()
        for a in A:
            bisect.insort(A2,a)
        A = A2



