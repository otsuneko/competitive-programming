N = int(input())

cnt = [0] # 10,100,1000,10000...以下の数字列が約数に持つ10の個数
d = 1
for i in range(18):
    cnt.append(d)
    d *= 10
print(cnt)

ans = 0
if N < 10:
    ans = 0
else:
    dig = len(str(N))
    for i in range(dig):
        if i == dig-1:
            ans += N*cnt[i]
        else:
            ans += cnt[i]
            N //= 10

print(ans)