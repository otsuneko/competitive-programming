# マッサージチェアのパワーを上げても大丈夫か
def check_if_ok(used,P,y,x):
    cur_pow = P[y][x]
    x1,y1,x2,y2 = max(0,x-cur_pow-1), max(0,y-cur_pow-1), min(N-1, x+cur_pow+1), min(N-1, y+cur_pow+1)

    # パワーを上げても大丈夫か
    for dy in range(y1,y2+1):
        for dx in range(x1,x2+1):
            if (abs(y-dy)+abs(x-dx) == cur_pow+1 and used[dy][dx] != 0):
                return False

    # 大丈夫なら、usedを更新
    for dy in range(y1,y2+1):
        for dx in range(x1,x2+1):
            if abs(y-dy)+abs(x-dx) <= cur_pow+1:
                used[dy][dx] = 1

    return True

def calc_score(E,P):
    score = 0
    for y in range(N):
        for x in range(N):
            score += E[y][x] * P[y][x]
    
    return score

N = int(input())
E = [list(map(int,input().split())) for _ in range(N)]
P = [[0]*N for _ in range(N)]

# ポイントが高い地点を探す
E2 = []
ave_score = 0
for y in range(N):
    for x in range(N):
        E2.append((E[y][x],y,x))
        ave_score += E[y][x]

E2.sort(reverse=True)
ave_score /= N**2
# print(ave_score)

# scoreが高い順に埋めていく
used = [[0]*N for _ in range(N)]
pre_score = 0
change_flag = False

while 1:
    for i,[s,y,x] in enumerate(E2):
        if not change_flag and i < N**2//2:
            break
        elif check_if_ok(used,P,y,x):
            P[y][x] += 1
    score = calc_score(E,P)

    if change_flag:
        if score == pre_score:
            break
        else:
            pre_score = score
    else:
        if score == pre_score:
            change_flag = True
        else:
            pre_score = score

# P出力
for y in range(N):
    print(*P[y])