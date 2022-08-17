# # 0-indexed
# def int_to_lower(k):
#     return chr(k+97)

# def lower_to_int(c):
#     return ord(c)-97

# N =int(input())
# s = list(input())
# alphabet = dict.fromkeys("abcdefghijklmnopqrstuvwxyz",0)
# for c in s:
#     alphabet[c] += 1
# s2 = sorted(s)
# mi = s2[0]

# l,r = 0,N-1
# while l < r:
#     if s[l] != mi:
#         if s[r] != mi:
#             alphabet[s[r]] -= 1
#             r -= 1
#         else:
#             s[l],s[r] = s[r],s[l]
#             alphabet[s[l]] -= 1
#             alphabet[s[r]] -= 1
#             l += 1
#             r -= 1
#             while alphabet[mi] == 0 and mi != "z":
#                 mi = int_to_lower(lower_to_int(mi)+1)
#     else:
#         alphabet[s[l]] -= 1
#         l += 1
#         while alphabet[mi] == 0 and mi != "z":
#             mi = int_to_lower(lower_to_int(mi)+1)

# print("".join(s))



# 区間に行う操作(最小値:min、最大値:max、区間和:x+y、区間積:x*y、最大公約数:gcd)
def segfunc(x, y):
    return min(x, y)

# 単位元(最小値:inf、最大値:-inf、区間和:0、区間積:1、最大公約数:0)
# 最小値/最大値はfloat("inf")を避けた方が高速化できる
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

'''
print(seg.query(0, 8))
seg.update(5, 0)
print(seg.query(0, 8))
'''

N = int(input())
s = input()

li = list(map(ord, s))
seg = SegTree(li, segfunc, ide_ele)
INF = 10**18
left,right = 0,N-1

while left < right:
    m = seg.query(left, right+1)
    m1 = seg.query(left+1, right+1)
    if li[left] > m1:
        while li[right] > m:
            seg.update(right, INF)
            right -= 1
        if li[left] > li[right]:
            li[left], li[right] = li[right] , li[left]
            seg.update(right, INF)
            right -= 1
    seg.update(left, INF)
    left += 1

print("".join(map(chr, li)))
