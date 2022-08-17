def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

def gcdlist(l):
    a = l[0]
    for n in l[1:]:
        a = gcd(a,n)
    return a

# K = int(input())
# from collections import defaultdict
# dict = defaultdict(int)

# ans = 0
# for a in range(1,K+1):
#     for b in range(1,K+1):
#         dict[gcd(a,b)] += 1

# for key in dict:
#     for c in range(1,K+1):
#         ans += gcd(key,c) * dict[key]

# print(ans)

# original answer
K = int(input())

ans = 0
for a in range(1,K+1):
    for b in range(1,K+1):
        for c in range(1,K+1):
            ans += gcdlist([a,b,c])

print(ans)