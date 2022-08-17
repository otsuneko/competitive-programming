A,B = map(int,input().split())
S = input()

flg = True
for i in range(len(S)):
    if i < A:
        if not S[i].isdigit():
            flg = False
            break
    elif i == A:
        if S[i] != "-":
            flg = False
            break
    else:
        if not S[i].isdigit():
            flg = False
            break
print(["No","Yes"][flg])