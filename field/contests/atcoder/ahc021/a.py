import sys
import time
import random
from copy import deepcopy

# 定数
TLE = 3
BEAM_RANGE = 1

# 状態管理用クラス
class State:
    def __init__(self, K, balls, moves):
        self.K = K
        self.score = 0
        self.balls = balls
        self.moves = moves

    # ボールを交換
    def change_balls(self,sx,sy,tx,ty):
        self.K += 1
        self.balls[sx][sy], self.balls[tx][ty] = self.balls[tx][ty], self.balls[sx][sy]
        state.moves.append((rx,ry,rx2,ry2))

    # スコア計算
    def calc_score(self):
        E = 0
        for x in range(N-1):
            for y in range(x+1):
                # 直下の2つのボールが自分の数値より大きいか判定
                if self.balls[x][y] > self.balls[x+1][y]:
                    E += 1
                if self.balls[x][y] > self.balls[x+1][y+1]:
                    E += 1
        
        if E == 0:
            self.score = 100000 - 5 * self.K
        else:
            self.score = 50000 - 50 * E

    # (sx,sy)の位置のボールと交換可能な隣接ボールのリストを取得
    def get_adjacent_balls(self,sx,sy):

        # 交換相手の候補
        cand_ball = set()

        # 追加可能な隣接ボールの座標判定
        if 0<=sx-1:
            if sy < sx:
                cand_ball.add((sx-1,sy))
            if 0<=sy-1:
                cand_ball.add((sx-1,sy-1))
        if 0<=sy-1:
            cand_ball.add((sx,sy-1))
        if sy+1<=sx:
            cand_ball.add((sx,sy+1))
        if sx+1<N:
            cand_ball.add((sx+1,sy))
            if sy+1<N:
                cand_ball.add((sx+1,sy+1))

        return list(cand_ball)

# 貪欲に交換すべきボールを決める
def decide_ori_ball(balls):
    #どういうボールを動かすべきか？
    #値が大きいにも関わらず上の方にいるボール
    #値が小さいにも関わらず下の方にいるボール
    cnt = 0
    dic = {}
    weight = []
    for x in range(N):
        for y in range(x+1):
            if balls[x][y] >= 450:
                priority = balls[x][y] / (x+1)
                dic[cnt] = (x,y)
                weight.append(priority)
                cnt += 1
            elif balls[x][y] < 50:
                priority = balls[x][y] * (x+1)
                dic[cnt] = (x,y)
                weight.append(priority)
                cnt += 1
    
    r = random.choices([i for i in range(cnt)],weights=weight,k=1)
    x,y = dic[r[0]]

    return x,y

# 貪欲に交換すべきボールを決める
def decide_ori_ball11(balls):
    #どういうボールを動かすべきか？
    #値が大きいにも関わらず上の方にいるボール
    #値が小さいにも関わらず下の方にいるボール
    cnt = 0
    dic = {}
    weight = []
    for x in range(N):
        for y in range(x+1):
            if 450 > balls[x][y] >= 400:
                priority = balls[x][y] / (x+1)
                dic[cnt] = (x,y)
                weight.append(priority)
                cnt += 1
            elif 50 <= balls[x][y] < 100:
                priority = balls[x][y] * (x+1)
                dic[cnt] = (x,y)
                weight.append(priority)
                cnt += 1
    
    r = random.choices([i for i in range(cnt)],weights=weight,k=1)
    x,y = dic[r[0]]

    return x,y

# 貪欲に交換すべきボールを決める
def decide_ori_ball12(balls):
    #どういうボールを動かすべきか？
    #値が大きいにも関わらず上の方にいるボール
    #値が小さいにも関わらず下の方にいるボール
    cnt = 0
    dic = {}
    weight = []
    for x in range(N):
        for y in range(x+1):
            if 400 > balls[x][y] >= 350:
                priority = balls[x][y] / (x+1)
                dic[cnt] = (x,y)
                weight.append(priority)
                cnt += 1
            elif 100 <= balls[x][y] < 150:
                priority = balls[x][y] * (x+1)
                dic[cnt] = (x,y)
                weight.append(priority)
                cnt += 1
    
    r = random.choices([i for i in range(cnt)],weights=weight,k=1)
    x,y = dic[r[0]]

    return x,y

def decide_ori_ball2(balls, state):
    #どういうボールを動かすべきか？
    #値が大きいにも関わらず上の方にいるボール
    #値が小さいにも関わらず下の方にいるボール
    cnt = 0
    dic = {}
    weight = []
    for x in range(N):
        for y in range(x+1):
            # 交換相手の候補
            cand_ball = state.get_adjacent_balls(x,y)

            for x2,y2 in cand_ball:
                #自分より上にいるのに値が大きい
                if x > x2 and balls[x2][y2] > balls[x][y]:
                    priority = abs(balls[x2][y2] - balls[x][y])
                    weight.append(priority)
                    dic[cnt] = (x,y)
                    cnt += 1
                #自分より下にいるのに値が小さい
                elif x < x2 and balls[x2][y2] < balls[x][y]:
                    priority = abs(balls[x][y] - balls[x2][y2])
                    weight.append(priority)
                    dic[cnt] = (x,y)
                    cnt += 1
    if cnt:
        r = random.choices([i for i in range(cnt)],weights=weight,k=1)
        x,y = dic[r[0]]
        return True,x,y
    else:
        return False,-1,-1
    
# 交換対象のボールを貪欲に決める
def decide_change_ball(ori_x,ori_y,balls,adj_balls):

    #どういうボールを交換すべきか？
    #自分より上にいるのに値が大きいor自分より下にいるのに値が小さい
    cnt = 0
    dic = {}
    weight = []
    for x,y in adj_balls:
        #自分より上にいるのに値が大きい
        if x < ori_x and balls[ori_x][ori_y] < balls[x][y]:
            priority = abs(balls[ori_x][ori_y] - balls[x][y])
            weight.append(priority)
            dic[cnt] = (x,y)
            cnt += 1
        #自分より下にいるのに値が小さい
        elif x > ori_x and balls[ori_x][ori_y] > balls[x][y]:
            priority = abs(balls[x][y] - balls[ori_x][ori_y])
            weight.append(priority)
            dic[cnt] = (x,y)
            cnt += 1
    
    if cnt:
        r = random.choices([i for i in range(cnt)],weights=weight,k=1)
        x,y = dic[r[0]]
        return True,x,y
    else:
        return False,-1,-1

# 計測開始
start = time.time()

# 入力
N = 30
balls = []
for _ in range(N):
    tmp = list(map(int,input().split()))
    balls.append(tmp)

# BEAM_RANGEの数だけstateを保持する
states = []
for _ in range(BEAM_RANGE):
    state = State(0,balls,[])
    state.calc_score()
    states.append((state.score, state))

while 1:

    # TLE対策
    now = time.time()
    if now - start > TLE * 0.9:
        break

    # ビームサーチ???
    for i in range(BEAM_RANGE):

        # TLE対策
        now = time.time()
        if now - start > TLE * 0.9:
            break

        score,state = states[i]

        # 交換元のボールを貪欲に決める
        if now - start < 0.3:
            rx,ry = decide_ori_ball(state.balls)
        elif now - start < 0.6:
            rx,ry = decide_ori_ball11(state.balls)
        elif now - start < 0.9:
            rx,ry = decide_ori_ball12(state.balls)
        else:
            flg,rx,ry = decide_ori_ball2(state.balls, state)
            if not flg:
                continue

        # 隣接するボールのリストを取得
        adj_balls = state.get_adjacent_balls(rx,ry)

        # 隣接ボールの中から交換相手を決める
        flg,rx2,ry2 = decide_change_ball(rx,ry,state.balls,adj_balls)

        if not flg:
            continue

        # ボールを交換する
        state.change_balls(rx,ry,rx2,ry2)

        # スコア計算
        state.calc_score()

        # パラメータ更新
        if state.score > score:
            states.append((state.score, deepcopy(state)))
        
    states.sort(key=lambda x:x[0], reverse=True)
    states = states[:BEAM_RANGE]

states.sort(key=lambda x:x[0], reverse=True)
final_score,final_state = states[0]

print(final_score,file=sys.stderr)
print(final_state.K)
for i in range(final_state.K):
    print(*final_state.moves[i])