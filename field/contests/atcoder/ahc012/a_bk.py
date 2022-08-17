import time
import random
import math

def check_FanShape(target_x, target_y, center_x, center_y, start_angle, end_angle, radius):

    # (0) 距離及び座標の準備
    distance_x = target_x- center_x
    distance_y = target_y- center_y
    start_x = math.cos(math.radians(start_angle))
    start_y = math.sin(math.radians(start_angle))
    end_x = math.cos(math.radians(end_angle))
    end_y = math.sin(math.radians(end_angle))

    # (1) その点は、扇形が属する円の中にあるか？
    # if distance_x ** 2 + distance_y ** 2 > radius** 2:
    #     return False
    # (2) 扇型の中心角は180°未満か？
    # 180°未満である場合
    if end_angle - start_angle < 180:
        # (3) その点が開始角より右側にあれば範囲外
        if start_x * distance_y - distance_x * start_y < 0:
            return False
        # (4) その点が終了角より左側にあれば範囲外 
        if end_x * distance_y - distance_x * end_y > 0:
            return False
        # 扇型の内部にある！
        return True 
    # 180°以上である場合
    else:
        # (3') その点が開始角より左側にあれば範囲外
        if start_x * distance_y - distance_x * start_y >= 0:
            return True
        # (4') その点は終了角より右側にあれば範囲外 
        if end_x * distance_y - distance_x * end_y <= 0:
            return True
        # 扇型の外部にある
        return False

def calc_score():

    li_angles = []
    for angle in angles:
        li_angles.append(angle)
        li_angles.append(angle+180)

    pieces = [0]*len(li_angles) # 各ピースに乗る苺の数を管理
    li_angles.sort()
    # print(li_angles)
    seen = set()
    for i in range(len(li_angles)):
        for x,y in pos:
            if (x,y) not in seen and check_FanShape(x, y, 0, 0, li_angles[i], li_angles[(i+1)%len(li_angles)], R):
                seen.add((x,y))
                pieces[i] += 1
    
    pieces.sort()
    # print(pieces)

    # スコア計算
    score = 0
    for d in range(10):
        a_d = A[d]
        b_d = pieces.count(d+1)
        score += 10**6 * min(a_d,b_d)/a_d

    score = round(score)
    return score

def cut_cake():

    # 原点を通り、もう一点を乱数で決めた直線でカット
    x,y = 0,0
    while 1:
        if len(angles):
            li_angles = sorted(list(angles))
            base_angle = li_angles[-1]
            theta = (base_angle + random.randint(1,5))%180
            # print(angles,theta)
        else:
            theta = random.randint(0,10)
        if theta not in angles:
            angles.add(theta)
            rad = math.radians(theta)
            x,y = round(R*math.cos(rad)),round(R*math.sin(rad))
            lines.add((x,y,0,0))
            break
    
    return  theta,(x,y,0,0)

R = 10**4
TLE = 5

N,K = map(int,input().split()) # K = 100
A = list(map(int,input().split()))
pos = [list(map(int,input().split())) for _ in range(N)]

start = time.time()
max_score = 0
max_lines = set()
while 1:

    now = time.time()
    if now-start > TLE:
        break

    # 何度も直線を引き直してベストのものを提出
    angles = set() # 原点を通る直線を角度で管理
    lines = set() # 直線を引くための円周上の点
    while 1:
        now = time.time()
        if now-start > TLE:
            break

        # 直線を引いてスコアが上がる限り引き続ける
        theta,cut_pos = cut_cake()

        # スコアを計算
        score = calc_score()
        if score >= max_score:
            max_score = score
            max_lines = lines
        else:
            angles.remove(theta)
            lines.remove(cut_pos)
        
        if len(lines)*2 == K:
            break

print(len(max_lines))
for lines in max_lines:
    print(*lines)