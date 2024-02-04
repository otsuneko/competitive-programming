import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

# BIT(Fenwick Tree) ※一点加算、区間和のRSQ相当
# https://qiita.com/toast-uz/items/bf6f142bace86c525532
class BIT:
    def __init__(self, n):
        self.n = len(n) if isinstance(n, list) else n
        self.size = 1 << (self.n - 1).bit_length()
        if isinstance(n, list):  # nは1-indexedなリスト
            a = [0]
            for p in n: a.append(p + a[-1])
            a += [a[-1]] * (self.size - self.n)
            self.d = [a[p] - a[p - (p & -p)] for p in range(self.size + 1)]
        else:                    # nは大きさ
            self.d = [0] * (self.size + 1)

    def __repr__(self):
        p = self.size
        res = []
        while p > 0:
            res2 = []
            for r in range(p, self.size + 1, p * 2):
                l = r - (r & -r) + 1
                res2.append(f'[{l}, {r}]:{self.d[r]}')
            res.append(' '.join(res2))
            p >>= 1
        res.append(f'{[self.sum(p + 1) - self.sum(p) for p in range(self.size)]}')
        return '\n'.join(res)

    def add(self, p, x):  # O(log(n)), 点pにxを加算
        assert p > 0
        while p <= self.size:
            self.d[p] += x
            p += p & -p

    def get(self, p, default=None):     # O(log(n))
        assert p > 0
        return self.sum(p) - self.sum(p - 1) if 1 <= p <= self.n or default is None else default

    def sum(self, p):     # O(log(n)), 閉区間[1, p]の累積和
        assert p >= 0
        res = 0
        while p > 0:
            res += self.d[p]
            p -= p & -p
        return res

    def lower_bound(self, x):   # O(log(n)), x <= 閉区間[1, p]の累積和 となる最小のp
        if x <= 0: return 0
        p, r = 0, self.size
        while r > 0:
            if p + r <= self.n and self.d[p + r] < x:
                x -= self.d[p + r]
                p += r
            r >>= 1
        return p + 1

'''
bit = BIT(5) # 要素数5個の配列を0で初期化
bit.add(1,3) # bit[1]に3を加算
bit.add(2,5) # bit[2]に5を加算
print(bit.sum(1,3)) # インデックス1から2(半閉半開区間)の要素の合計(=8)を取得
print(bit.d) # [0,3,5,8,0]
'''

# 転倒数を求める（必要ならAは座圧しておく）
def get_inversion_num(A):
    ma = max(A)
    bit = BIT(ma)
    res = 0
    for a in A:
        # 「aより左にあるaより大きい数」の個数を足す
        res += bit.sum(ma) - bit.sum(a)
        bit.add(a, 1)
    return res



H,W = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]
B = [list(map(int,input().split())) for _ in range(H)]

import itertools

ans = INF
for ptr_H in itertools.permutations([i for i in range(H)], H):
    ptr_H = list(ptr_H)
    A2 = [a[:] for a in A]
    for i,y in enumerate(ptr_H):
        for x in range(W):
            A2[i][x] = A[y][x]

    for ptr_W in itertools.permutations([i for i in range(W)], W):
        ptr_W = list(ptr_W)
        A3 = [a[:] for a in A2]
        for y in range(H):
            for i,x in enumerate(ptr_W):
                A3[y][x] = A2[y][i]
        
        if A3 == B:
            for i in range(len(ptr_H)):
                ptr_H[i] += 1
            for i in range(len(ptr_W)):
                ptr_W[i] += 1
            ans = min(ans,get_inversion_num(ptr_H)+get_inversion_num(ptr_W))
        
if ans == INF:
    print(-1)
else:
    print(ans)