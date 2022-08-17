from itertools import groupby, zip_longest
S = input()
T = input()

grpS = groupby(S)
grpT = groupby(T)

for s,t in zip_longest(grpS,grpT):
    if s == None or t == None:
        print("No")
        exit()
    if s[0] != t[0]:
        print("No")
        exit()
    lenS = len(list(s[1]))
    lenT = len(list(t[1]))
    if (lenS==1 and lenT>1) or lenS > lenT:
        print("No")
        exit()
print("Yes")