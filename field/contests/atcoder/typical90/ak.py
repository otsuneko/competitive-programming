# 区間に行う操作(最小値:min、最大値:max、区間和:x+y、区間積:x*y、最大公約数:gcd)
def segfunc(x, y):
    return max(x, y)

# 単位元(最小値:inf、最大値:-inf、区間和:0、区間積:1、最大公約数:0)
# 最小値/最大値はinfを避けた方が高速化できる
ide_ele = -1

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

W,N =map(int,input().split())
dish =[list(map(int,input().split())) for _ in range(N)]

dp = [[-1]*(W+1) for _ in range(N+1)]
for i in range(N+1):
    dp[i][0] = 0

for i in range(1,N+1):
    seg = SegTree(dp[i-1], segfunc, ide_ele)
    L,R,V = dish[i-1]
    for j in range(W+1):
        #選ばない
        dp[i][j] = dp[i-1][j]
        #選ぶ
        ma = seg.query(max(0,j-R), max(0,j-L+1))
        if ma >= 0:
            dp[i][j] = max(dp[i][j], ma+V)
print(dp[N][W])