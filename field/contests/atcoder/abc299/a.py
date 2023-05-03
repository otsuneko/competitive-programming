N = int(input())
S = input()

cnt = 0
flg = False
for i in range(N):
    if not flg and S[i] == "|":
        flg = True
    elif flg and S[i] == "*":
        cnt += 1
    elif flg and S[i] == "|":
        flg = False

if cnt > 0:
    print("in")
else:
    print("out")