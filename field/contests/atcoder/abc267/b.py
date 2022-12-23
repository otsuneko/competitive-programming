S = input()

flg = [False]*7

if S[6] == "1":
    flg[0] = True
if S[3] == "1":
    flg[1] = True
if S[1] == "1" or S[7] == "1":
    flg[2] = True
if S[0] == "1" or S[4] == "1":
    flg[3] = True
if S[2] == "1" or  S[8] == "1":
    flg[4] = True
if S[5] == "1":
    flg[5] = True
if S[9] == "1":
    flg[6] = True

if S[0] == "1":
    print("No")
    exit()

cnt = 0
for f in flg:
    if cnt == 0 and f:
        cnt += 1
    if cnt == 1 and not f:
        cnt += 1
    if cnt == 2 and f:
        print("Yes")
        exit()
print("No")