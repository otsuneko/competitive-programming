import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''

N = int(input())
A = list(map(int,input().split()))
A.sort()
import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))
# cumsum = list(itertools.accumulate(A[::-1], func=operator.add))[::-1] + [0] # 逆順の累積和
# print(A)

ans = 0
for i in range(N-1):
    base = 10**8 - A[i]
    ans += cumsum[-1] - cumsum[i+1] + A[i]*(N-1-i)

    idx = bisect_left(A, base)
    # print(idx)
    if idx > i:
        ans -= 10**8 * (N-idx)
    else:
        ans -= 10**8 * (N-i-1)
    # print(ans)

print(ans)
