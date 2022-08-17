N = int(input())

money = 0
i = 1
while 1:
    money += i
    if money >= N:
        print(i)
        exit()
    i += 1
