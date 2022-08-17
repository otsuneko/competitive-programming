import math
mod = 10**9 + 7
# x ** a をmodで割った余りを、O(log(a))時間で求める。
def power(x, a):
    if a == 0:
        return 1
    elif a == 1:
        return x
    elif a % 2 == 0:
        return power(x, a//2) **2 % mod
    else:
        return power(x, a//2) **2 * x % mod

# xの逆元を求める。フェルマーの小定理より、 x の逆元は x ^ (mod - 2) に等しい。計算時間はO(log(mod))程度。
def modinv(x):
    return power(x, mod-2)

# nCrをmodで割った余りを計算
def nCr(n, r):
    numera = 1  # 分子
    denomi = 1  # 分母

    for i in range(r):
        numera *= n-i
        numera %= mod
        denomi *= i+1
        denomi %= mod
    return numera * modinv(denomi) % mod

N,M,K = map(int,input().split())

if K >= N:
    if N > M:
        print(nCr(N+M,N))
    else:
        print(nCr(N+M,M))
else:
    