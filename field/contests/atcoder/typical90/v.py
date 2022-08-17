def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

def gcdlist(l):
    a = l[0]
    for i in range(len(l)):
        a = gcd(a,l[i])
    return a

A,B,C = map(int,input().split())
n = gcdlist([A,B,C])
ans = A//n + B//n + C//n - 3
print(ans)