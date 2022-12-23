# 区間に行う操作(最小値:min、最大値:max、区間和:x+y、区間積:x*y、最大公約数:gcd)
def segfunc(x, y):
    return min(x, y)

#単位元(最小値:inf、最大値:-inf、区間和:0、区間積:1、最大公約数:0)
ide_ele = float('inf')

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

Q = int(input())
N = 2**20
A = [-1]*2*N
seg = SegTree(A, segfunc, ide_ele)

def is_ok(mid,x):
    if seg.query(x,mid) == -1:
        return True
    else:
        return False

def meguru_bisect(ng, ok,x):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid,x):
            ok = mid
        else:
            ng = mid
    return ok

for _ in range(Q):
    t,x = map(int,input().split())

    if t == 1:
        idx = meguru_bisect(-1,2*N,x%N)-1
        # print("idx:",idx)
        if idx < N:
            seg.update(idx%N,x)
            seg.update(idx%N+N,x)
            A[idx] = x
        else:
            seg.update(idx%N,x)
            seg.update(idx,x)
            A[idx%N] = x
    elif t == 2:
        print(A[x%N])
        # print(A[:10])