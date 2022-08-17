N = int(input())
A = list(map(int,input().split()))
total = sum(A)
A += A

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))

import bisect

for i in range(N):
    idx = bisect.bisect_left(cumsum, cumsum[i] + total/10)
    if cumsum[idx] == cumsum[i] + total/10:
        print("Yes")
        break
else:
    print("No")

# N = int(input())
# A = list(map(int,input().split()))
# total = sum(A)
# if total//10 != total/10:
#     print("No")
#     exit()

# A += A

# from collections import deque

# q=deque()
# s = 0
# for c in A:
#     q.append(c)  ## dequeの右端に要素を一つ追加する。
#     s += c

#     if s == total//10:
#         print("Yes")
#         exit()

#     while not s <= total//10:
#         rm=q.popleft() ## 条件を満たさないのでdequeの左端から要素を取り除く
#         s -= rm
#         if s == total//10:
#             print("Yes")
#             exit()
# print("No")