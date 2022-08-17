X = int(input())

money = 100
ans = 0
while money < X:
    money += money//100
    ans += 1
print(ans)
