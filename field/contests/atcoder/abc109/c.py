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

N,X = map(int,input().split())
Xs = list(map(int,input().split()))

diff = []
for x in Xs:
    diff.append(abs(x-X))
print(gcdlist(diff))