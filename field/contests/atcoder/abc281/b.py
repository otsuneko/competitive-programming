S = input()

if len(S) != 8:
    print("No")
    exit()

for i,s in enumerate(S):
    if i == 0 or i == 7:
        if not s.isalpha():
            print("No")
            exit()
    else:
        if not s.isdigit():
            print("No")
            exit()

if not 100000 <= int(S[1:7]) <= 999999:
    print("No")
    exit()
print("Yes")