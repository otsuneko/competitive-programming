# 区間に行う操作(最小値:min、最大値:max、区間和:x+y、区間積:x*y、最大公約数:gcd)
def segfunc_max(x, y):
    return max(x, y)

# 区間に行う操作(最小値:min、最大値:max、区間和:x+y、区間積:x*y、最大公約数:gcd)
def segfunc_min(x, y):
    return min(x, y)

# 単位元(最小値:inf、最大値:-inf、区間和:0、区間積:1、最大公約数:0)
# 最小値/最大値はfloat('inf')を避けた方が高速化できる
ide_ele_max = -10**18

# 単位元(最小値:inf、最大値:-inf、区間和:0、区間積:1、最大公約数:0)
# 最小値/最大値はfloat('inf')を避けた方が高速化できる
ide_ele_min = 10**18

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

N,X,Y = map(int,input().split())
A = list(map(int,input().split()))

seg_max = SegTree(A, segfunc_max, ide_ele_max)
seg_min = SegTree(A, segfunc_min, ide_ele_min)

def is_ok_ma(l,r):
    ma = seg_max.query(l,r)
    if ma > X:
        return True
    else:
        return False

def meguru_bisect_ma(ng, ok,l):
    while (abs(ok - ng) > 1):
        r = (ok + ng) // 2
        if is_ok_ma(l,r):
            ok = r
        else:
            ng = r
    return ok

def is_ok_mi(l,r):
    mi = seg_min.query(l,r)
    if mi < Y:
        return True
    else:
        return False

def meguru_bisect_mi(ng, ok,l):
    while (abs(ok - ng) > 1):
        r = (ok + ng) // 2
        if is_ok_mi(l,r):
            ok = r
        else:
            ng = r
    return ok


ans = 0
for l in range(N):
    r_ma = meguru_bisect_ma(l-1,N,l)
    r_mi = meguru_bisect_mi(l-1,N,l)
    print(r_ma,r_mi)
    r = min(r_ma,r_mi)
    if l<=r and seg_max.query(l,r) == X and seg_min.query(l,r) == Y:
        ans += r-l+1

print(ans)