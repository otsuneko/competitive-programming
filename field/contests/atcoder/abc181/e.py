# 区間に行う操作(最小値:min、最大値:max、区間和:x+y、区間積:x*y、最大公約数:gcd)
def segfunc(x, y):
    return x+y

# 単位元(最小値:inf、最大値:-inf、区間和:0、区間積:1、最大公約数:0)
# 最小値/最大値はfloat('inf')を避けた方が高速化できる
ide_ele = 0

class SegTree:
    """
    init(init_val, segfunc,ide_ele): 配列init_valで初期化 O(N)
    update(k, x): k番目の値をxに更新 O(N)
    query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
    """
    def __init__(self, init_val, segfunc, ide_ele):
        """
        n: 要素数
        num: n以上の最小の2のべき乗
        tree: セグメント木(1-index)
        """
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1 << (n - 1).bit_length()
        self.tree = [ide_ele] * 2 * self.num
        # 配列の値を葉にセット
        for i in range(n):
            self.tree[self.num + i] = init_val[i]
        # 構築していく
        for i in range(self.num - 1, 0, -1):
            self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, k, x):
        """
        k番目の値をxに更新
        k: index(0-index)
        x: update value
        """
        k += self.num
        self.tree[k] = x
        while k > 1:
            self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
            k >>= 1

    def query(self, l, r):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
        res = self.ide_ele

        l += self.num
        r += self.num
        while l < r:
            if l & 1:
                res = self.segfunc(res, self.tree[l])
                l += 1
            if r & 1:
                res = self.segfunc(res, self.tree[r - 1])
            l >>= 1
            r >>= 1
        return res

'''
print(seg.query(0, 8))
seg.update(5, 0)
print(seg.query(0, 8))
'''

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''

N,M = map(int,input().split())
H = list(map(int,input().split()))
W = list(map(int,input().split()))
H.sort()

pdiff = []
for i in range(0,N,2):
    if i+1 < N:
        pdiff.append(H[i+1]-H[i])
pdiff2 = []
for i in range(1,N,2):
    pdiff2.append(H[i+1]-H[i])

seg = SegTree(pdiff, segfunc, ide_ele)
seg2 = SegTree(pdiff2, segfunc, ide_ele)
for i in range(N//2):
    seg.update(i,pdiff[i])
    seg2.update(i,pdiff2[i])

# print(pdiff,pdiff2)

ans = 10**18
for w in W:
    idx = bisect_left(H,w)
    # print(idx)
    if idx%2:
        diff = w - H[idx-1]
        if idx == N:
            ans = min(ans, seg.query(0,N//2)+diff)
        else:
            ans = min(ans, seg.query(0,idx//2)+diff+seg2.query(idx//2,N//2))
    else:
        diff = H[idx] - w
        ans = min(ans, seg.query(0,idx//2)+diff+seg2.query(idx//2,N//2))
print(ans)