N = int(input())
S = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ans = ""
while N//36 > 0:
    ans += S[N%36]
    N //= 36
else:
    ans += S[N]
print(ans[::-1])