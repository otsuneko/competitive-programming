N = int(input())
S = [input() for _ in range(N)]

check = set()

for s in S:
    if s[0] not in ["H","D","C","S"]:
        print("No")
        exit()
    elif s[1] not in ["A","2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "T" , "J" , "Q" , "K"]:
        print("No")
        exit()
    if s in check:
        print("No")
        exit()
    check.add(s)

print("Yes")