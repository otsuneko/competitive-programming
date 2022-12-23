from collections import defaultdict
from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport
Q = int(input())
dict = defaultdict(int)
hq_mi = []
hq_ma = []

for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        x = query[1]
        if dict[x] == 0:
            heappush(hq_mi,x)
            heappush(hq_ma,-x)
        dict[x] += 1
    elif query[0] == 2:
        x,c = query[1:]
        if c >= dict[x] and dict[x]:
            dict[x] = 0
        else:
            dict[x] -= c
    else:
        mi = ma = 0
        while 1:
            mi = heappop(hq_mi)
            if dict[mi] > 0:
                heappush(hq_mi,mi)
                break
        while 1:
            ma = -heappop(hq_ma)
            if dict[ma] > 0:
                heappush(hq_ma,-ma)
                break
        print(ma-mi)

# from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
# from collections import defaultdict
# Q = int(input())
# dict = defaultdict(int)
# li = []

# for _ in range(Q):
#     query = list(map(int,input().split()))
#     if query[0] == 1:
#         x = query[1]
#         if dict[x] == 0:
#             insort(li,x)
#         dict[x] += 1
#     elif query[0] == 2:
#         x,c = query[1:]
#         if c >= dict[x]:
#             if dict[x] > 0:
#                 li.remove(x)
#                 dict[x] = 0
#         else:
#             dict[x] -= c
#     else:
#         print(li[-1]-li[0])