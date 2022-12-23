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

# K 個の青いボールと N−K 個の赤いボール
N,K = map(int,input().split())

for i in range(1,K+1):
    ans = 1

    # 青をiグループに分ける通り数
    ans = nCr(K-1,i-1)

    # 青のグループを赤の横にねじこむ通り数
    ans = ans * nCr(N-K+1,i) % mod
    print(ans)