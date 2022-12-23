mod = 998244353
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

N,K =map(int,input().split())

ans = 0
half = -(-(N)//2)
if K < half:
    ans = 0
else:
    ans = nCr(N-half,K-half)

print(ans)