mod = 10**9 + 7
# xの逆元を求める。フェルマーの小定理より、 x の逆元は x ^ (mod - 2) に等しい。計算時間はO(log(mod))程度。
def modinv(x):
    return pow(x,mod-2,mod)

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

n = int(input())
k = int(input())

ans = nCr(n,k)
print(ans)

def pos(x, n, m):
    if n == 0:
        return 1
    res = pos(x*x%m, n//2, m)
    if n%2 == 1:
        res = res*x%m
    return res