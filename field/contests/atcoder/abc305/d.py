N = int(input())
A = list(map(int,input().split()))
Q = int(input())

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''
# print(cumsum)
for _ in range(Q):
    l,r = map(int,input().split())
    s = bisect_left(cumsum,l)
    t = bisect_right(cumsum,r)
    # print(s,t)

    ans = 0
    if s%2:
        ans += cumsum[s] - l
    else:
        ans += cumsum[s+1] - l
    if t%2:
        ans += r - cumsum[t-1]
    print(ans)