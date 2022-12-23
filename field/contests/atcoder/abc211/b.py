S1 = input()
S2 = input()
S3 = input()
S4 = input()

check = set([])
check.add(S1)
check.add(S2)
check.add(S3)
check.add(S4)

if len(check) == 4:
    print("Yes")
else:
    print("No")
