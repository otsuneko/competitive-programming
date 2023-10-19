import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M,P = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''
A.sort()
B.sort()

import itertools
import operator
cumsum = [0] + list(itertools.accumulate(B, func=operator.add))
# cumsum = list(itertools.accumulate(A[::-1], func=operator.add))[::-1] + [0] # 逆順の累積和

ans = 0
for a in A:
    idx = bisect(B,P-a)
    ans += (a*idx + cumsum[idx]) + P*(M-idx)

print(ans)