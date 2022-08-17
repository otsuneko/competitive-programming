import itertools

num =list(map(int,input().split()))
mi = 10**18
ma = -10**18

for cmb in itertools.combinations(num,2):
    mul = cmb[0]*cmb[1]
    if mul < mi:
        mi = mul
    if mul > ma:
        ma = mul

print(mi,ma)