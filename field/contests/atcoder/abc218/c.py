# 二次元配列の90度右回転
def rotate_2d(arr):
    res = []
    for r in zip(*arr[::-1]):
        res.append(r)
    return res

N = int(input())
S = [list(input()) for _ in range(N)]
T = [list(input()) for _ in range(N)]

S2 = []
inv_S = list(zip(*S))
flag = True
for s in inv_S:
    if s.count("#") == 0 and flag:
        continue
    else:
        S2.append(s)
        flag = False
inv_S2 = list(zip(*S2))
S_trim = []
flag = True
for s in inv_S2:
    if s.count("#") == 0 and flag:
        continue
    else:
        S_trim.append(s)
        flag = False

check_S = set()
for y in range(len(S_trim)):
    for x in range(len(S_trim[y])):
        if S_trim[y][x] == "#":
            check_S.add((x,y))

for i in range(4):
    T = rotate_2d(T)
    T2 = []
    inv_T = list(zip(*T))
    flag = True
    for t in inv_T:
        if t.count("#") == 0 and flag:
            continue
        else:
            T2.append(t)
            flag = False
    inv_T2 = list(zip(*T2))
    T_trim = []
    flag = True
    for t in inv_T2:
        if t.count("#") == 0 and flag:
            continue
        else:
            T_trim.append(t)
            flag = False
    
    check_T = set()
    for y in range(len(T_trim)):
        for x in range(len(T_trim[y])):
            if T_trim[y][x] == "#":
                check_T.add((x,y))
    if check_S == check_T:
        print("Yes")
        exit()
print("No")