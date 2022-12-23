N = int(input())
A = list(map(int,input().split()))

ma = max(A)
ans = 0
max_gcd = 0
for i in range(2,ma+1):
    gcd = 0
    for a in A:
        if a%i == 0:
            gcd += 1
    if gcd > max_gcd:
        ans = i
        max_gcd = gcd
print(ans)