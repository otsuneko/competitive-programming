S = list(input())
inv_S = S[::-1]
l = len(S)

cnt_f = 0
for i in range(l):
    if S[i] == "a":
        cnt_f += 1
    else:
        break

cnt_b = 0
for i in reversed(range(l)):
    if S[i] == "a":
        cnt_b += 1
    else:
        break

if cnt_b == 0:
    if S == inv_S:
        print("Yes")
        exit()
else:
    if S[cnt_f:l-cnt_b] == S[cnt_f:l-cnt_b][::-1] and cnt_f <= cnt_b:
        print("Yes")
        exit()

print("No")