S = input()

xB,yB = 0,0
flgB = False
xR,yR = 0,0
flgR = False
z = 0
for i in range(len(S)):
    if not flgB:
        if S[i] == "B":
            xB = i
            flgB = True
    else:
        if S[i] == "B":
            yB = i

    if not flgR:
        if S[i] == "R":
            xR = i
            flgR = True
    else:
        if S[i] == "R":
            yR = i

    if S[i] == "K":
        z = i

if xB%2 != yB%2 and (xR < z < yR):
    print("Yes")
else:
    print("No")
