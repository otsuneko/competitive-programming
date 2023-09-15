from typing import List
import sys
import time
import random
from heapq import *  # heapqライブラリのimport
from collections import defaultdict
import math

def debug(*args): print(*args, file=sys.stderr)

# 定数
TIME_LIMIT = 4.0
INF = 10**18
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1]) #縦横移動

class Pos:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

# ジャッジとのやり取り用クラス
class Judge:
    # 空調設備の温度設定
    def set_temperature(self, temperature: List[List[int]]) -> None:
        for row in temperature:
            print(" ".join(map(str, row)))
        sys.stdout.flush()

    # 温度計測
    def measure(self, i: int, y: int, x: int) -> int:
        print(f"{i} {y} {x}", flush=True)
        v = int(input())
        if v == -1:
            print(f"something went wrong. i={i} y={y} x={x}", file=sys.stderr)
            sys.exit(1)
        return v

    # ワームホールと出口セルの対応関係の回答
    def answer(self, estimate: List[int]) -> None:
        print("-1 -1 -1")
        for e in estimate:
            print(e)
        sys.stdout.flush()

# ここに回答を実装
class Solver:

    def __init__(self, L: int, N: int, S: int, exit_pos: List[Pos]):
        self.start = time.time()
        self.L = L
        self.N = N
        self.S = S
        self.exit_pos = exit_pos
        self.judge = Judge()

        # i番目のワームホールから通じる出口セルの周囲で実際に計測された温度
        self.measured_temp = [[] for _ in range(self.N)]

        self.BOX_WIDTH = self.BOX_HEIGHT = 2
        if self.L >= 43:
            self.BOX_WIDTH = self.BOX_HEIGHT = 3
        if self.S >= 500 and self.N >= 90:
            self.BOX_WIDTH = self.BOX_HEIGHT = 3
        if self.S == 900 or (self.S >= 750 and self.N >= 90):
            self.BOX_WIDTH = self.BOX_HEIGHT = 4

        self.MEASURE_ORDER = [] # 出口セル周囲マスの相対座標を温度測定の順番に並べる(だいたい出口セルから近い順に測定するため)
        self.MEASURE_SIZE = 6
        for dist in range(self.MEASURE_SIZE):
            for y in range(-self.MEASURE_SIZE, self.MEASURE_SIZE+1):
                for x in range(-self.MEASURE_SIZE, self.MEASURE_SIZE+1):
                    if max(abs(y),abs(x)) == dist:
                        self.MEASURE_ORDER.append((y,x))

        self.MIN_TEMP = 0 # 温度設定の最小値
        self.MAX_TEMP = 1000 # 温度設定の最大値
        if S >= 700:
            self.MIN_TEMP,self.MAX_TEMP = 200, 1000
        elif S >= 500:
            self.MIN_TEMP,self.MAX_TEMP = 400, 1000
        elif S >= 400:
            self.MIN_TEMP,self.MAX_TEMP = 400, 1000
        elif S >= 289:
            self.MIN_TEMP,self.MAX_TEMP = 500, 1000
        elif S >= 196:
            self.MIN_TEMP,self.MAX_TEMP = 500, 1000
        elif S >= 100:
            self.MIN_TEMP,self.MAX_TEMP = 700, 1000
        elif S >= 50:
            self.MIN_TEMP,self.MAX_TEMP = 750, 1000
        elif S in [36,49]:
            self.MIN_TEMP,self.MAX_TEMP = 700, 850
        elif S in [9,16,25]:
            self.MIN_TEMP,self.MAX_TEMP = 700, 800
        elif S in [1,4]:
            self.MIN_TEMP,self.MAX_TEMP = 500, 530

        self.DEFAULT_TEMP = (self.MIN_TEMP + self.MAX_TEMP)//2 # 温度設定のデフォ値

        # ある出口セル周囲マスの温度計測の度に、あるワームホールが何回連続で最も類似していれば
        # その出口セルと対応付くと判定できるかの閾値
        self.CONSECUTIVE_WIN_CNT = 60
        if self.S == 1:
            self.CONSECUTIVE_WIN_CNT = 7
        elif self.S == 4:
            self.CONSECUTIVE_WIN_CNT = 10
        elif self.S == 9:
            self.CONSECUTIVE_WIN_CNT = 12
        elif self.S == 16:
            self.CONSECUTIVE_WIN_CNT = 13
        elif self.S == 25:
            self.CONSECUTIVE_WIN_CNT = 15
        elif self.S == 36:
            self.CONSECUTIVE_WIN_CNT = 19
        elif self.S == 49:
            self.CONSECUTIVE_WIN_CNT = 21
        elif self.S == 64:
            self.CONSECUTIVE_WIN_CNT = 23
        elif self.S == 81:
            self.CONSECUTIVE_WIN_CNT = 23
        elif self.S == 100:
            self.CONSECUTIVE_WIN_CNT = 26
        elif self.S == 121:
            self.CONSECUTIVE_WIN_CNT = 28
        elif self.S == 144:
            self.CONSECUTIVE_WIN_CNT = 30
        elif self.S == 169:
            self.CONSECUTIVE_WIN_CNT = 32
        elif self.S == 196:
            self.CONSECUTIVE_WIN_CNT = 32
        elif self.S == 225:
            self.CONSECUTIVE_WIN_CNT = 34
        elif self.S == 256:
            self.CONSECUTIVE_WIN_CNT = 36
        elif self.S == 289:
            self.CONSECUTIVE_WIN_CNT = 38
        elif self.S == 324:
            self.CONSECUTIVE_WIN_CNT = 40
        elif self.S == 361:
            self.CONSECUTIVE_WIN_CNT = 40
        elif self.S == 400:
            self.CONSECUTIVE_WIN_CNT = 40
        elif self.S == 441:
            self.CONSECUTIVE_WIN_CNT = 40
        elif self.S == 484:
            self.CONSECUTIVE_WIN_CNT = 40
        elif self.S >= 500:
            self.CONSECUTIVE_WIN_CNT = 50
        elif self.S >= 750:
            self.CONSECUTIVE_WIN_CNT = 60

        # ある出口セル周囲マスに最も類似しているワームホールと、次に類似しているワームホールの
        # 距離の比率の閾値
        self.DIST_RATIO = 0.8

    def solve(self) -> None:
        temperature = self._create_temperature()
        self.judge.set_temperature(temperature)
        estimate = self._predict(temperature)
        self.judge.answer(estimate)

    # 温度設定する
    def _create_temperature(self) -> List[List[int]]:
        
        investigation_pos = set() # 温度測定対象となる各出口セル周囲マスの座標の集合
        temperature = [[self.DEFAULT_TEMP] * self.L for _ in range(self.L)] # グリッド上の設定温度を保持

        # 各出口セル周囲の温度の初期値を設定
        for i, pos in enumerate(self.exit_pos):
            for dy in range(-self.BOX_HEIGHT, self.BOX_HEIGHT+1, 1):
                for dx in range(-self.BOX_WIDTH, self.BOX_WIDTH+1, 1):
                    ny,nx = (pos.y+dy) % self.L, (pos.x+dx) % self.L
                    investigation_pos.add((ny,nx))

                    # Sの値に応じて各出口セル周囲マスの設定温度を保存
                    if self.S >= 500:
                        temp = random.choices([self.MIN_TEMP,self.MAX_TEMP], weights=[45,55])[0]
                        temperature[ny][nx] = temp
                    elif self.S >= 300:
                        temp = random.choice([self.MIN_TEMP,self.DEFAULT_TEMP,self.MAX_TEMP])
                        temperature[ny][nx] = temp
                    elif self.S >= 50:                        
                        temp = random.randint(self.MIN_TEMP,self.MAX_TEMP)
                        temperature[ny][nx] = temp
                    else:
                        # Sが小さい場合、左上をMIN_TEMP~MAX_TEMPの乱数値で初期化して一定値(例：5)ずつ乱数で上下させることで設置コスト減
                        if dy == -self.BOX_HEIGHT and dx == -self.BOX_WIDTH:
                            temp = random.randint(self.MIN_TEMP,self.MAX_TEMP)
                        else:
                            RANGE = self.S**0.5 * 3
                            r = random.randint(-RANGE,RANGE)
                            pre = temperature[ny-1][nx] if dx == -self.BOX_WIDTH else temperature[ny][nx-1]
                            temp = pre + r if 0 <= pre + r <= 1000 else pre - r
                        temperature[ny][nx] = temp

        # 温度計測対象外マスの温度を周囲との差が最小化できるように設定し直す
        for _ in range(1000):
            for y in range(self.L):
                for x in range(self.L):
                    if (y,x) in investigation_pos:
                        continue
                    su = 0
                    for dy,dx in MOVE:
                        su += temperature[(y+dy)%self.L][(x+dx)%self.L]**2
                    temperature[y][x] = int((su // 4)**0.5)

        return temperature

    # ワームホールと出口セルの対応を予想
    def _predict(self, temperature: List[List[int]]) -> List[int]:

        # i番目のワームホールがどの出口セルに対応しているかの予測値
        estimate = [-1] * self.N
        # 累計温度計測回数
        total_measure_cnt = 0
        # 累計温度計測コスト
        # total_measure_cost = 0
        matched = set() # 既に対応づいた出口を保存
        # 出口セル周囲マスの計測温度を初期化
        self.measured_temp = [[] for _ in range(self.N)]
        for enter_id in range(self.N):
            # ある出口セルの周囲マスを繰り返し温度計測する。
            # 各回の計測終了後に、判明した温度情報から予め温度設定した
            # どの出口セルとの距離が最も近いかを判定。
            # 最も近い距離が他の距離と比較して明確に小さければ正しく対応づいたと判定。
            champion = []
            for cnt, (dy,dx) in enumerate(self.MEASURE_ORDER):
                # 温度計測上限回数に達した場合は終了
                if total_measure_cnt == 10000:
                    break

                # 温度計測
                measured_value = self.judge.measure(enter_id, dy, dx)
                total_measure_cnt += 1
                # total_measure_cost += 100 * (10 + abs(dy) + abs(dx))
                # 計測結果を記録
                self.measured_temp[enter_id].append(measured_value)

                # その回の温度計測までの情報を基に、出口セルを判定できるか？
                dists = [[INF,-1] for _ in range(self.N)]
                min_dist = second_min_dist = INF
                for exit_id in range(self.N):
                    if exit_id in matched:
                        continue
                    dist = 0
                    for idx,(dy,dx) in enumerate(self.MEASURE_ORDER[:len(self.measured_temp[enter_id])]):
                        enter_temp = self.measured_temp[enter_id][idx]
                        exit_y, exit_x = (self.exit_pos[exit_id].y + dy) % self.L, (self.exit_pos[exit_id].x + dx) % self.L
                        exit_temp = temperature[exit_y][exit_x]
                        dist += abs(enter_temp - exit_temp)
                        # 枝刈り
                        if dist > second_min_dist:
                            dists[exit_id] = [INF,exit_id]
                            break
                    else:
                        if dist < min_dist:
                            second_min_dist = min_dist
                            min_dist = dist
                        elif dist < second_min_dist:
                            second_min_dist = dist
                        dists[exit_id] = [dist,exit_id]
                
                # 判定
                dists.sort()
                champion.append(dists[0][1])
                # print(enter_id, dists[:5], file=sys.stderr)
                if len(champion) >= self.CONSECUTIVE_WIN_CNT and len(set(champion[-self.CONSECUTIVE_WIN_CNT:])) == 1 and dists[0][0]/dists[1][0] < self.DIST_RATIO:
                    estimate[enter_id] = champion[-1]
                    matched.add(champion[-1])
                    break

            # print(enter_id, self.total_measure_cnt, file=sys.stderr)
                        
        # 予め設定した温度と最も類似度の高い出口セルを対応付ける
        estimate = self._match_probable_pairs(temperature,estimate)
        
        return estimate
    
    # 最も類似度の高い出口セルを探す
    def _match_probable_pairs(self, temperature, estimate):
        # i番目のワームホールから入って調査した周囲マスと、予め設定した各出口マス周囲の温度ごとの類似度を計算
        hq = []
        used = set()
        cnt = 0
        for enter_id in range(self.N):
            # 既に対応づいているワームホールはスキップ
            if estimate[enter_id] != -1:
                used.add(estimate[enter_id])
                cnt += 1
                continue
            for exit_id in range(self.N):
                dist = self._calc_dist(enter_id, exit_id, temperature)
                heappush(hq, (dist, enter_id, exit_id))

        # 全てのワームホールが相異なる出口セルと対応づくまで、類似度が高い順に対応付けていく
        while hq:
            # print("used:",len(used),"N:",self.N, file=sys.stderr)
            if cnt == self.N:
                break

            dist, enter_id, exit_id = heappop(hq)
            if estimate[enter_id] == -1 and exit_id not in used:
                estimate[enter_id] = exit_id
                used.add(exit_id)
                cnt += 1
        
        return estimate

    # 周囲マスの値を特徴ベクトルとして距離計算
    def _calc_dist(self, enter_id, exit_id, temperature):
        dist = 0
        for idx,(dy,dx) in enumerate(self.MEASURE_ORDER[:len(self.measured_temp[enter_id])]):
            enter_temp = self.measured_temp[enter_id][idx]
            exit_y, exit_x = (self.exit_pos[exit_id].y + dy) % self.L, (self.exit_pos[exit_id].x + dx) % self.L
            exit_temp = temperature[exit_y][exit_x]
            dist += abs(enter_temp - exit_temp)
    
        # print(enter_id, exit_id, dist, file=sys.stderr)
        return dist

def main():
    L, N, S = [int(v) for v in input().split(" ")]
    exit_pos = []
    for _ in range(N):
        y, x = (int(v) for v in input().split(" "))
        exit_pos.append(Pos(y, x))

    solver = Solver(L, N, S, exit_pos)
    solver.solve()


if __name__ == "__main__":
    main()
