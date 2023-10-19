def lower_to_int(c):
    return ord(c)-97

S = input()
T = input()

change = [[False]*26 for _ in range(26)]

for s,t in zip(S,T):
    s = lower_to_int(s)
    t = lower_to_int(t)
    change[s][t] = True

for i in range(26):
    cnt = cnt2 = 0
    for j in range(26):
        if change[i][j]:
            cnt += 1
        if change[j][i]:
            cnt2 += 1
        if cnt >= 2 or cnt2 >= 2:
            print("No")
            exit()

print("Yes")