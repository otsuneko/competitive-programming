def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

L,R = map(int,input().split())
ans = 0

x,y = L,R
while x < L+10**6:
    while y > x:
        if gcd(x,y) == 1:
            ans = max(ans,y-x)
            break
        y -= 1
    x += 1

x,y = L,R
while y > R-10**6:
    while y > x:
        if gcd(x,y) == 1:
            ans = max(ans,y-x)
            break
        x += 1
    y -= 1

print(ans)
