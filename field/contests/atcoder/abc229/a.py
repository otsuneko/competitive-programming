S1 = input()
S2 = input()

idx = 0
if S1.count("#") == 1:
    idx = S1.index("#")
    if S2.count("#") == 1 and S2.index("#") != idx:
        print("No")
        exit()
print("Yes")