def gcd(a, b):
    cnt = 0
    if b == 0:
        print(cnt)
        return a
    else:
        print(b,a%b)
        cnt+=1
        return gcd(b, a % b)

A, B = map(int, input().split())
cnt = 0

while A >= 1 and B >= 1:
    g = gcd(A, B)
    A -= g
    B -= g
    cnt += 1
    exit()

print(cnt)
