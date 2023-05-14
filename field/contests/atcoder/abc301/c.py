alphaS = dict.fromkeys("abcdefghijklmnopqrstuvwxyz@",0)
alphaT = dict.fromkeys("abcdefghijklmnopqrstuvwxyz@",0)

S = list(input())
T = list(input())

for s in S:
    alphaS[s] += 1

for t in T:
    alphaT[t] += 1

for key in alphaS:
    if key == "@":
        continue
    if key in "atcoder":
        if alphaS[key] < alphaT[key]:
            diff = alphaT[key] - alphaS[key]
            if alphaS["@"] < diff:
                print("No")
                exit()
            alphaS["@"] -= diff
            alphaS[key] += diff
    else:
        if alphaS[key] != alphaT[key]:
            print("No")
            exit()

for key in alphaT:
    if key == "@":
        continue
    if key in "atcoder":
        if alphaT[key] < alphaS[key]:
            diff = alphaS[key] - alphaT[key]
            if alphaT["@"] < diff:
                print("No")
                exit()
            alphaT["@"] -= diff
            alphaT[key] += diff
    else:
        if alphaS[key] != alphaT[key]:
            print("No")
            exit()

print("Yes")