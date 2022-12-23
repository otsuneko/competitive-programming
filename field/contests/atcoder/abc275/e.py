from fractions import Fraction

mod = 998244353
def modinv(x):
    return pow(x,mod-2,mod)

N,M,K = map(int,input().split())

# k回目にどこにいるかの通り数
dp = [[0]*(N+1) for _ in range(K+1)]
dp[0][0] = 1

for k in range(K):
    for n in range(N):
        for m in range(1,M+1):
            if n+m > N:
                dp[k+1][2*N-(n+m)] = (dp[k+1][2*N-(n+m)] + dp[k][n])%mod
            else:
                dp[k+1][(n+m)] = (dp[k+1][(n+m)] + dp[k][n])%mod

frac = Fraction()
for k in range(K+1):
    frac += Fraction(dp[k][N],pow(M,k,mod))

# print(*dp, sep="\n")

# print(cnt)
print(modinv(frac.denominator)*frac.numerator%mod)