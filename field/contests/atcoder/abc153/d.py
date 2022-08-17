H = int(input())

ans = 0
cnt = 1
while H > 0:
    H = H//2
    ans += cnt
    cnt *= 2
print(ans)