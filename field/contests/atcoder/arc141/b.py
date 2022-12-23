def rec(i,cnt):
    if cnt == p+1:
        return 0

    ret = 0
    left = 2**(i-1)
    for j in range(i+1,p+2):
        right = 2**(j-1) if j != p+1 else M-2**(j-1)+1
        # print(left,right,j)
        ret += (rec(j,cnt+1) + left * right) % mod

    return ret

N,M = map(int,input().split())
mod = 998244353

p = 0
while N:
    N //= 2
    p += 1

if M < 2**p:
    print(0)
    exit()

ans = 0
for i in range(1,p+2):
    ans = (ans + rec(i,0))%mod

print(ans)