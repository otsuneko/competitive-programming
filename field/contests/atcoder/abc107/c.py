from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''

N,K = map(int,input().split())
X = list(map(int,input().split()))
X.sort()

zidx = bisect(X,0)
print(X,zidx)

ans = 10**18
l = r = 0
if zidx >= K:
    l = max(0,zidx-K)
    r = l+K-1
    ans = -X[0]
# elif zidx == 0