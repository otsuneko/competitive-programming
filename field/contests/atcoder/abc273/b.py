from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

X,K = map(int,input().split())

s = '1'
for k in range(K+1):
    X = Decimal(str(X)).quantize((Decimal(s)), rounding=ROUND_HALF_UP)
    s = '1E' + str(k+1)

print(int(X))