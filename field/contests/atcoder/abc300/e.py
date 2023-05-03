# https://github.com/wanidon/python-modint/blob/master/modint.py
MOD = 998244353
class ModInt:

    def __init__(self, x):
        self.x = x.x if isinstance(x, ModInt) else x % MOD

    __str__ = lambda self:str(self.x)
    __repr__ = __str__
    __int__ = lambda self: self.x
    __index__ = __int__

    __add__ = lambda self, other: ModInt(self.x + ModInt(other).x)
    __sub__ = lambda self, other: ModInt(self.x - ModInt(other).x)
    __mul__ = lambda self, other: ModInt(self.x * ModInt(other).x)
    __pow__ = lambda self, other: ModInt(pow(self.x, ModInt(other).x, MOD))
    __truediv__ = lambda self, other: ModInt(self.x * pow(ModInt(other).x, MOD - 2, MOD))
    __floordiv__ = lambda self, other: ModInt(self.x // ModInt(other).x)
    __radd__ = lambda self, other: ModInt(other + self.x)
    __rsub__ = lambda self, other: ModInt(other - self.x)
    __rpow__ = lambda self, other: ModInt(pow(other, self.x, MOD))
    __rmul__ = lambda self, other: ModInt(other * self.x)
    __rtruediv__ = lambda self, other: ModInt(other * pow(self.x, MOD - 2, MOD))
    __rfloordiv__ = lambda self, other: ModInt(other // self.x)

    __lt__ = lambda self, other: self.x < ModInt(other).x
    __gt__ = lambda self, other: self.x > ModInt(other).x
    __le__ = lambda self, other: self.x <= ModInt(other).x
    __ge__ = lambda self, other: self.x >= ModInt(other).x
    __eq__ = lambda self, other: self.x == ModInt(other).x
    __ne__ = lambda self, other: self.x != ModInt(other).x

# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

iP = 1 / ModInt(5)
memo = dict()
def dfs(n):
    if n >= N:
        return 1 if n == N else 0
    
    if n in memo:
        return memo[n]

    res = ModInt(0)
    for i in range(2,7):
        res += dfs(i*n)
    memo[n] = res*iP
    return memo[n]

N = int(input())

print(dfs(1))

# 確率MOD典型
# ModIntを用いて確率をDP/メモ化再帰で計算する
# iP = 1 / ModInt(P)　のように分母をModIntで計算しておき、
# dp[i][j][0] *= iPのように逆元として乗算すると計算量からlogが取れて高速らしい
# ターン制2人ゲームの場合は、dp[i][j][f]のfでAのターン→Bのターン(またその逆)の遷移を表現してゴールから計算
# 参考提出
# E - Dice Product 3 (https://atcoder.jp/contests/abc300/submissions/41068136)
# E - Unfair Sugoroku (https://atcoder.jp/contests/abc298/submissions/41068068)