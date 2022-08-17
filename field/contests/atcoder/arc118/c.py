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

N = int(input())

base = [2*3,2*5,3*5]

ans = base[:]
for b in base:
    for m in range(2,2000):
        if b*m > 10000:
            break
        if b*m not in ans:
            ans.append(b*m)

print(*ans[:N])