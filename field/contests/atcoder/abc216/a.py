X = input()
num = X.split(".")

if 0 <= int(num[1]) <= 2:
    print(str(num[0]) + "-")
elif 3 <= int(num[1]) <= 6:
    print(str(num[0]))
else:
    print(str(num[0]) + "+")