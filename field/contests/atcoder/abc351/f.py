import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

# 式変形解法
A2 = sorted(A)
ans = 0
for i,a in enumerate(A2):
    ans += a * i

for i,a in enumerate(A):
    ans -= a * (N-1-i)

print(ans)

# 平面走査解法
# # 区間に行う操作(最小値:min、最大値:max、区間和:x+y、区間積:x*y、最大公約数:gcd)
# def segfunc(x, y):
#     return x+y

# # 単位元(最小値:inf、最大値:-inf、区間和:0、区間積:1、最大公約数:0)
# # 最小値/最大値はfloat('inf')を避けた方が高速化できる
# ide_ele = 0

# class SegTree:
#     """
#     init(init_val, segfunc,ide_ele): 配列init_valで初期化 O(N)
#     update(k, x): k番目の値をxに更新 O(N)
#     query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
#     """
#     def __init__(self, init_val, segfunc, ide_ele):
#         """
#         n: 要素数
#         num: n以上の最小の2のべき乗
#         tree: セグメント木(1-index)
#         """
#         n = len(init_val)
#         self.segfunc = segfunc
#         self.ide_ele = ide_ele
#         self.num = 1 << (n - 1).bit_length()
#         self.tree = [ide_ele] * 2 * self.num
#         # 配列の値を葉にセット
#         for i in range(n):
#             self.tree[self.num + i] = init_val[i]
#         # 構築していく
#         for i in range(self.num - 1, 0, -1):
#             self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])

#     def update(self, k, x):
#         """
#         k番目の値をxに更新
#         k: index(0-index)
#         x: update value
#         """
#         k += self.num
#         self.tree[k] = x
#         while k > 1:
#             self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
#             k >>= 1

#     def query(self, l, r):
#         """
#         [l, r)のsegfuncしたものを得る
#         l: index(0-index)
#         r: index(0-index)
#         """
#         res = self.ide_ele

#         l += self.num
#         r += self.num
#         while l < r:
#             if l & 1:
#                 res = self.segfunc(res, self.tree[l])
#                 l += 1
#             if r & 1:
#                 res = self.segfunc(res, self.tree[r - 1])
#             l >>= 1
#             r >>= 1
#         return res

#     def __getitem__(self, k):
#         "k番目の値を取得"
#         if not (0 <= k < self.n): raise IndexError
#         return self.tree[self.num + k]

# # 引数となるリストはソート不要かつ値の重複可(内部処理で対応するため)
# def compress(arr):
#     *XS, = set(arr)
#     XS.sort()
#     return {e: i for i, e in enumerate(XS)}

# N = int(input())
# A = list(map(int,input().split()))
# comp_A = compress(A)

# li = [0]*N
# seg_num = SegTree(li, segfunc, ide_ele)
# seg_sum = SegTree(li, segfunc, ide_ele)

# ans = 0
# # 逆順でiを固定して見ていく
# for a in A[::-1]:
#     idx = comp_A[a]
#     seg_num.update(idx, seg_num.query(idx, idx+1)+1)
#     seg_sum.update(idx, seg_sum.query(idx, idx+1)+a)
#     num = seg_num.query(idx+1, N)
#     su = seg_sum.query(idx+1, N)
#     ans += su - num*a

# print(ans)
