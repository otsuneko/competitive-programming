import itertools
import operator
N,M,K = map(int,input().split())
mod = 998244353

if K == 0:
    print(pow(M,N,mod))
    exit()

dp = [[0]*M for _ in range(N)]

for i in range(M):
    dp[0][i] = 1

for i in range(N-1):
    cumsum = [0] + list(itertools.accumulate(dp[i], func=operator.add))
    for j in range(M):
        # Kより下に離れているケース
        if j - K >= 0:
            dp[i+1][j] = (dp[i+1][j] + cumsum[j-K+1])%mod
        # Kより上に離れているケース
        if j + K <= M:
            dp[i+1][j] = (dp[i+1][j] + cumsum[M]-cumsum[j+K])%mod

# print(*dp, sep="\n")
print(sum(dp[N-1])%mod)



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

# N,M,K = map(int,input().split())
# mod = 998244353

# if K == 0:
#     print(pow(M,N,mod))
#     exit()

# dp = [[0]*M for _ in range(N)]

# for i in range(M):
#     dp[0][i] = 1
# seg = SegTree(dp[0], segfunc, ide_ele)

# for i in range(N-1):
#     for j in range(M):
#         # Kより下に離れているケース
#         if j - K >= 0:
#             # print("low",j,seg.query(0,j-K+1))
#             dp[i+1][j] = (dp[i+1][j] + seg.query(0,j-K+1))%mod
#         # Kより上に離れているケース
#         if j + K <= M:
#             # print("high",j,seg.query(j+K,M+1))
#             dp[i+1][j] = (dp[i+1][j] + seg.query(j+K,M+1))%mod
#     seg = SegTree(dp[i+1], segfunc, ide_ele)

# # print(*dp, sep="\n")
# print(sum(dp[N-1])%mod)