import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from bisect import bisect_left

class BitVector:
    def __init__(self, size):
        # self.BLOCK_WIDTH = 32
        self.BLOCK_NUM = (size + 31) >> 5
        self.bit = [0] * self.BLOCK_NUM
        self.count = [0] * self.BLOCK_NUM

    def __getitem__(self, i):
        return (self.bit[i >> 5] >> (i & 31)) & 1

    def set(self, i):
        self.bit[i >> 5] |= 1 << (i & 31)

    def build(self):
        for i in range(self.BLOCK_NUM - 1):
            self.count[i + 1] = self.count[i] + self.popcount(self.bit[i])

    def popcount(self, x):
        x = x - ((x >> 1) & 0x55555555)
        x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
        x = (x + (x >> 4)) & 0x0f0f0f0f
        x = x + (x >> 8)
        x = x + (x >> 16)
        return x & 0x0000007f

    def rank1(self, r):
        mask = (1 << (r & 31)) - 1
        return self.count[r >> 5] + self.popcount(self.bit[r >> 5] & mask)

    def rank0(self, r):
        mask = (1 << (r & 31)) - 1
        return r - (self.count[r >> 5] + self.popcount(self.bit[r >> 5] & mask))


class RectangleSum:
    def __init__(self, array, ws, MAXLOG=32):
        self.MAXLOG = MAXLOG
        self.n = len(array)
        self.mat = []
        self.zs = []
        self.data = [[0] * (self.n + 1) for _ in range(self.MAXLOG)]

        order = [i for i in range(self.n)]
        for d in reversed(range(self.MAXLOG)):
            vec = BitVector(self.n + 1)
            ls = []
            rs = []
            for i, val in enumerate(order):
                if array[val] & (1 << d):
                    rs.append(val)
                    vec.set(i)
                else:
                    ls.append(val)
            vec.build()
            self.mat.append(vec)
            self.zs.append(len(ls))
            order = ls + rs
            for i, val in enumerate(order):
                self.data[- d - 1][i + 1] = self.data[- d - 1][i] + ws[val]

    def rect_sum(self, l, r, upper):
        res = 0
        for d in range(self.MAXLOG):
            if upper >> (self.MAXLOG - d - 1) & 1:
                res += self.data[d][self.mat[d].rank0(r)]
                res -= self.data[d][self.mat[d].rank0(l)]
                l = self.mat[d].rank1(l) + self.zs[d]
                r = self.mat[d].rank1(r) + self.zs[d]
            else:
                l = self.mat[d].rank0(l)
                r = self.mat[d].rank0(r)
        return res

# [l,r)の範囲内にあるwがupper未満の要素のwの合計を計算
# pointsは各要素が[x,y,w]で表されるリスト
class CompressedRectangleSum:
    def __init__(self, points):
        points = sorted(points)
        self.xs, ys, ws = zip(*points)
        self.ys = sorted(set(ys))
        self.comp = {val: idx for idx, val in enumerate(self.ys)}
        ys = [self.comp[val] for val in ys]
        MAXLOG = len(self.ys).bit_length()
        self.mat = RectangleSum(ys, ws, MAXLOG)

    def rect_sum(self, l, r, upper):
        l = bisect_left(self.xs, l)
        r = bisect_left(self.xs, r)
        upper = bisect_left(self.ys, upper)
        return self.mat.rect_sum(l, r, upper)

N = int(input())
A = list(map(int,input().split()))
pts = []
for i,a in enumerate(A):
    pts.append((i,a,a))
crs = CompressedRectangleSum(pts)

Q = int(input())
ans = 0
for _ in range(Q):
    a,b,c = map(int,input().split())
    l,r,x = a^ans, b^ans, c^ans
    l -= 1
    ans = crs.rect_sum(l,r,x+1)
    print(ans)
