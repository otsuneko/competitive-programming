N = int(input())
S =[list(input()) for _ in range(N)]
S_inv = list(zip(*S))

ans = False
for h in range(N):
    for w in range(N):
        if w+5 < N and S[h][w:w+6].count("#") >= 4:
            ans = True
            break
        if w+5 < N and S_inv[h][w:w+6].count("#") >= 4:
            ans = True
            break
        cnt1 = cnt2 = 0
        cntd1 = cntd2 = 0
        for i in range(6):
            if h+i < N and w+i < N:
                if S[h+i][w+i] == "#":
                    cnt1 += 1
                else:
                    cntd1 += 1
            if h+i < N and 0 <= w-i:
                if S[h+i][w-i] == "#":
                    cnt2 += 1
                else:
                    cntd2 += 1
        if (cnt1 + cntd1 == 6 and cnt1 >= 4) or (cnt2 + cntd2 == 6 and cnt2 >= 4):
            ans = True
            break
print(["No","Yes"][ans])