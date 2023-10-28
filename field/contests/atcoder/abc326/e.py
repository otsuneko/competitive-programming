import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

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

N = int(input())
A = list(map(int,input().split()))

# 確率MOD典型
# ModIntを用いて確率をDP/メモ化再帰で計算する
# iP = 1 / ModInt(P)のように予め分母をModIntで計算しておき、
# dp[i][j][0] *= iPのように逆元として乗算する(dpの値は分子が取りうる通り数の数え上げ)
# ※ターン制2人ゲームの場合は、dp[i][j][f]のfでAのターン→Bのターン(またその逆)の遷移を表現してゴールから計算
# 参考提出
# E - Dice Product 3 (https://atcoder.jp/contests/abc300/submissions/41068136)
# E - Unfair Sugoroku (https://atcoder.jp/contests/abc298/submissions/41068068)

iP = 1 / ModInt(N)
dp = [0]*(N+1) # k回試行した時の給料の期待値
import itertools
import operator
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))
# cumsum = list(itertools.accumulate(A[::-1], func=operator.add))[::-1] + [0] # 逆順の累積和

for i in range(N):
    dp[i+1] = (dp[i] + cumsum[N-i]) * (i+1) * (iP**(N-i))

print(dp[N])