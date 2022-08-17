def digsum(n):
    res = 0
    while n > 0:
        res += 1
        n //= 10
    
    return res
N = int(input())
keta = digsum(N)

ans = 0
for i in range(1,keta):
    if i%2:
        ans += 10**i - 10**(i-1)

if keta%2:
    ans += N-10**(keta-1)+1

print(ans)