L,R = map(int,input().split())
mod = 10**9+7

dig_L = dig_R = 0
L2,R2 = L,R
while L2 > 0:
    dig_L += 1
    L2 //= 10

while R2 > 0:
    dig_R += 1
    R2 //= 10

ans = 0
if dig_L == dig_R:
    S = (R-L+1) * (L+R) // 2
    ans = (ans + dig_L * S) % mod
else:
    S_L = (10**dig_L-L) * (L+10**dig_L-1) // 2
    ans = (ans + dig_L * S_L) % mod
    S_R = (R-10**(dig_R-1)+1) * (R+10**(dig_R-1)) // 2
    ans = (ans + dig_R * S_R) % mod

for i in range(dig_L,dig_R-1):
    S = (10**(i+1) - 10**i) * (10**(i+1)-1 + 10**i) // 2
    ans = (ans + (i+1) * S) % mod

print(ans)