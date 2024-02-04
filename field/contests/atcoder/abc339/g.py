import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

# from bisect import bisect_left

# class BitVector:
#     def __init__(self, size):
#         # self.BLOCK_WIDTH = 32
#         self.BLOCK_NUM = (size + 31) >> 5
#         self.bit = [0] * self.BLOCK_NUM
#         self.count = [0] * self.BLOCK_NUM

#     def __getitem__(self, i):
#         return (self.bit[i >> 5] >> (i & 31)) & 1

#     def set(self, i):
#         self.bit[i >> 5] |= 1 << (i & 31)

#     def build(self):
#         for i in range(self.BLOCK_NUM - 1):
#             self.count[i + 1] = self.count[i] + self.popcount(self.bit[i])

#     def popcount(self, x):
#         x = x - ((x >> 1) & 0x55555555)
#         x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
#         x = (x + (x >> 4)) & 0x0f0f0f0f
#         x = x + (x >> 8)
#         x = x + (x >> 16)
#         return x & 0x0000007f

#     def rank1(self, r):
#         mask = (1 << (r & 31)) - 1
#         return self.count[r >> 5] + self.popcount(self.bit[r >> 5] & mask)

#     def rank0(self, r):
#         mask = (1 << (r & 31)) - 1
#         return r - (self.count[r >> 5] + self.popcount(self.bit[r >> 5] & mask))


# class RectangleSum:
#     def __init__(self, array, ws, MAXLOG=32):
#         self.MAXLOG = MAXLOG
#         self.n = len(array)
#         self.mat = []
#         self.zs = []
#         self.data = [[0] * (self.n + 1) for _ in range(self.MAXLOG)]

#         order = [i for i in range(self.n)]
#         for d in reversed(range(self.MAXLOG)):
#             vec = BitVector(self.n + 1)
#             ls = []
#             rs = []
#             for i, val in enumerate(order):
#                 if array[val] & (1 << d):
#                     rs.append(val)
#                     vec.set(i)
#                 else:
#                     ls.append(val)
#             vec.build()
#             self.mat.append(vec)
#             self.zs.append(len(ls))
#             order = ls + rs
#             for i, val in enumerate(order):
#                 self.data[- d - 1][i + 1] = self.data[- d - 1][i] + ws[val]

#     def rect_sum(self, l, r, upper):
#         res = 0
#         for d in range(self.MAXLOG):
#             if upper >> (self.MAXLOG - d - 1) & 1:
#                 res += self.data[d][self.mat[d].rank0(r)]
#                 res -= self.data[d][self.mat[d].rank0(l)]
#                 l = self.mat[d].rank1(l) + self.zs[d]
#                 r = self.mat[d].rank1(r) + self.zs[d]
#             else:
#                 l = self.mat[d].rank0(l)
#                 r = self.mat[d].rank0(r)
#         return res

# # [l,r)の範囲内にあるwがupper未満の要素のwの合計を計算
# # pointsは各要素が[x,y,w]で表されるリスト
# class CompressedRectangleSum:
#     def __init__(self, points):
#         points = sorted(points)
#         self.xs, ys, ws = zip(*points)
#         self.ys = sorted(set(ys))
#         self.comp = {val: idx for idx, val in enumerate(self.ys)}
#         ys = [self.comp[val] for val in ys]
#         MAXLOG = len(self.ys).bit_length()
#         self.mat = RectangleSum(ys, ws, MAXLOG)

#     def rect_sum(self, l, r, upper):
#         l = bisect_left(self.xs, l)
#         r = bisect_left(self.xs, r)
#         upper = bisect_left(self.ys, upper)
#         return self.mat.rect_sum(l, r, upper)

# N = int(input())
# A = list(map(int,input().split()))
# pts = []
# for i,a in enumerate(A):
#     pts.append((i,a,a))
# crs = CompressedRectangleSum(pts)

# Q = int(input())
# ans = 0
# for _ in range(Q):
#     a,b,c = map(int,input().split())
#     l,r,x = a^ans, b^ans, c^ans
#     l -= 1
#     ans = crs.rect_sum(l,r,x+1)
#     print(ans)

# 区間に行う操作(最小値:min、最大値:max、区間和:x+y、区間積:x*y、最大公約数:gcd)
def segfunc(x, y):
    return min(x, y)

# 単位元(最小値:inf、最大値:-inf、区間和:0、区間積:1、最大公約数:0)
# 最小値/最大値はfloat('inf')を避けた方が高速化できる
ide_ele = 10**18

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

    def __getitem__(self, k):
        "k番目の値を取得"
        if not (0 <= k < self.n): raise IndexError
        return self.tree[self.num + k]


from bisect import bisect
from itertools import accumulate

# SegmentTreeにソート済みの配列を乗せる
# 累積和も持たせることで[l,r)の要素のうちx以下のものの総和を取得する
# https://atcoder.jp/contests/abc339/submissions/49976903
class MergeSortTree:
    def __init__(self, init_val):
        self.n = len(init_val)
        self.tree = [[] for _ in range(self.n)] + [[x] for x in init_val]
        self.cumsum = [[] for _ in range(self.n)] + [[x] for x in init_val]
        for i in range(self.n-1, -1, -1):
            self.tree[i] = self.merge(self.tree[i<<1], self.tree[i<<1|1])
            self.cumsum[i] = list(accumulate(self.tree[i]))

    def merge(self, li1, li2):
        i,j = 0,0
        res = []
        while i<len(li1) and j<len(li2):
            if li1[i] <= li2[j]:
                res.append(li1[i])
                i += 1
            else:
                res.append(li2[j])
                j += 1
        res += li1[i:] + li2[j:]
        return res

    # [l,r)の要素のうちx以下のものの総和を取得
    def sum_le_x(self, l, r, x):
        l += self.n
        r += self.n
        su = 0
        while l<r:
            if l&1:
                i = bisect(self.tree[l], x)
                if i: su += self.cumsum[l][i-1]
                l += 1
            if r&1:
                r -= 1
                i = bisect(self.tree[r], x)
                if i: su += self.cumsum[r][i-1]
            l >>= 1
            r >>= 1
        return su

N = int(input())
li = list(map(int,input().split()))
seg = MergeSortTree(li)

Q = int(input())
ans = 0
for _ in range(Q):
    a,b,c = map(int,input().split())
    l,r,x = a^ans, b^ans, c^ans
    ans = seg.sum_le_x(l-1, r, x)
    print(ans)