from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
from collections import defaultdict
dict = defaultdict(list)

N =int(input())
A = list(map(int,input().split()))
Q = int(input())

for i,a in enumerate(A):
    dict[a].append(i)

for _ in range(Q):
    L,R,X =map(int,input().split())
    L,R = L-1,R-1
    li = dict[X]
    if len(li) == 0:
        print(0)
    elif len(li) == 1:
        if L <= li[0] <= R:
            print(1)
        else:
            print(0)
    else:
        l = bisect_left(li,L)
        r = bisect(li,R)
        print(r-l)