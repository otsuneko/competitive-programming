def rolling(s, n):
    l = len(s)
    #右にシフトの場合
    return s[-n%l:] + s[:-n%l] #左にシフトの場合はnの正負を逆に

xyz = input()

print(int(xyz) + int(rolling(xyz,1)) + int(rolling(xyz,2)))