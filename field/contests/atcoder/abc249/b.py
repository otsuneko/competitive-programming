S = input()

isup = islow = False
for s in S:
    if s.isupper():
        isup = True
    elif s.islower():
        islow = True

if len(set(S)) == len(S) and isup and islow:
    print("Yes")
else:
    print("No")