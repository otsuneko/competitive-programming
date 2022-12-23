def rolling(s, n):
    l = len(s)
    #右にシフトの場合
    return s[-n%l:] + s[:-n%l] #左にシフトの場合はnの正負を逆に

mi = "z"*1000
ma = "a"
S = input()

for _ in range(len(S)+1):
    S = rolling(S,1)
    if S < mi:
        mi = S
    if S > ma:
        ma = S

print(mi)
print(ma)