from fractions import Fraction

mod = 998244353
def modinv(x):
    return pow(x,mod-2,mod)

N,P = map(int,input().split())

dp = [0]*(N+2)
dp[0] = Fraction(1)

for i in range(N):
    frac = dp[i]
    dp[i+1] += Fraction((i+1)*(100-P)*frac.numerator, 100*frac.denominator)

    dp[i+2] += Fraction((i+1)*P*frac.numerator, 100*frac.denominator)

    print(dp)

frac = Fraction(dp[N+1].numerator + dp[N].numerator, dp[N+1].denominator + dp[N].denominator)
print(frac)
print(modinv(frac.denominator)*frac.numerator%mod)