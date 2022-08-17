import math
S = input()
mod = 998244353

ans = 0
for l in range(1,len(S)):
    mul = len(S)-l+1
    for i in range(math.ceil((len(S)-l+1)/2)):
        l = int(S[i:i+l])
        r = int(S[len(S)-l-i:len(S)-i])
        if l == r:
            ans += l * mul % mod
        else:
            ans += l * mul % mod
            ans += r * mul % mod

        mul -= 1

print(ans)