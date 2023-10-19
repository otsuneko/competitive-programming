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

        # 正規分布の累積密度関数を計算
        # self.normalCDF = [0]*2001
        # mean = 0
        # stddev = self.S
        # for t in range(-1000,1001):
        #     self.normalCDF[t+1000] = 0.5 * (1.0 + math.erf((t - mean) / (stddev * math.sqrt(2.0))))
        
        # 1点だけ高温にする座標とその温度
        #TODO: どの出口セルからも一番近い座標を高温にする
        self.high_y, self.high_x = self.L//2, self.L//2
        self.high_temperature = 1000

        # 各出口セルから中心座標(1点だけ温度を上げる点)までの距離
        self.dists_to_center = [[-1,-1,-1,-1] for _ in range(self.N)]
        for i, pos in enumerate(exit_pos):
            dy,dx = self.high_y-pos.y, self.high_x-pos.x
            dist = abs(dy) + abs(dx)
            self.dists_to_center[i] = [i,dist,dy,dx]
        self.dists_to_center.sort(key=lambda x:x[1])

    def solve(self) -> None:
        temperature = self._create_temperature()
        self.judge.set_temperature(temperature)
        estimate = self._predict(temperature)
        self.judge.answer(estimate)

    # 座標y,xで、温度lowからhighを出力する確率
    # def _get_prob(self, y, x, low, high, temperature):
    #     res = self.normalCDF(high, temperature[y][x]) - self.normalCDF(low ,temperature[y][x])
    #     if low == 0:
    #         res = self.normalCDF(high, temperature[y][x]) - 0
    #     if high == 1000:
    #         res = 1 - self.normalCDF(low ,temperature[y][x])
    #     return res

    # 温度設定する
    def _create_temperature(self) -> List[List[int]]:
        temperature = [[0] * self.L for _ in range(self.L)] # グリッド上の設定温度を保持
        #TODO: Sの値に応じて温度を何度にするか決定する
        temperature[self.high_y][self.high_x] = self.high_temperature
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

        # 各出口セルから1点高温地点の方向に移動し温度調査する
        # 計測される温度xは平均self.high_temperature、標準偏差がself.S**0.5の正規分布に従うとする
        # 実際の温度θはself.high_temperature、標準偏差が1の正規分布に従うとする
        sigma = 1
        for enter_id in range(self.N):
            # 温度の期待値
            expected_temperature = [0]*self.N
            for exit_id,dist,dy,dx in self.dists_to_center:

                if exit_id in matched:
                    continue

                # 温度計測
                measure_cnt = 1 if self.S < 100 else 3
                measure_result = []
                for _ in range(measure_cnt):
                    # 温度計測上限回数に達した場合は終了
                    if total_measure_cnt == 10000:
                        break
                    measured_value = self.judge.measure(enter_id, dy, dx)
                    measure_result.append(measured_value)
                    # debug(measured_value)
                    total_measure_cnt += 1
                    # total_measure_cost += 100 * (10 + abs(dy) + abs(dx))

                # 実際の温度θの事後分布の期待値
                mean_measured_value = sum(measure_result)/measure_cnt
                expected_temperature[exit_id] = (self.high_temperature / (sigma**2) + mean_measured_value / (self.S)) / (1/(sigma**2) + measure_cnt/self.S)

            # debug(expected_temperature)
            min_diff = INF
            min_id = -1
            for exit_id in range(self.N):
                if abs(self.high_temperature - expected_temperature[exit_id]) < min_diff:
                    min_diff = abs(self.high_temperature - expected_temperature[exit_id])
                    min_id = exit_id
            estimate[enter_id] = min_id
            matched.add(min_id)
        
        return estimate

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
