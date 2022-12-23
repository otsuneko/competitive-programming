Y = int(input())

for y in range(Y,3010):
    if y%4 == 2:
        print(y)
        exit()