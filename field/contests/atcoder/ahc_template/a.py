from typing import List
import sys
import time
import random

# 定数
TIME_LIMIT = 4.0
INF = 10**18
BOX_SIZE = 5 # 出口セルの周囲何マスを調査するか
MIN_TEMP = 100 # 温度設定の最小値
MAX_TEMP = 500 # 温度設定の最大値

class Pos:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

# 空調設備の温度設定、検査、回答用クラス
class Judge:
    # 空調設備の温度設定
    def set_temperature(self, temperature: List[List[int]]) -> None:
        for row in temperature:
            print(" ".join(map(str, row)))
        sys.stdout.flush()

    # 温度計測
    # TODO: BOX_SIZE分の周囲マスを計測
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


class Solver:

    def __init__(self, L: int, N: int, S: int, exit_pos: List[Pos]):
        self.L = L
        self.N = N
        self.S = S
        self.exit_pos = exit_pos
        self.judge = Judge()

    def solve(self) -> None:
        temperature = self._create_temperature()
        self.judge.set_temperature(temperature)
        estimate = self._predict(temperature)
        self.judge.answer(estimate)

    # 温度設定する
    # TODO:出口セルの周囲5*5マスの温度分布を特徴的にする。それ以外のセルは一旦0とかにしとけばいい。
    # まずはめんどいからランダムに設定、しよう！！
    def _create_temperature(self) -> List[List[int]]:
        temperature = [[0] * self.L for _ in range(self.L)]
        for i, pos in enumerate(self.exit_pos):
            for dy in range(-BOX_SIZE, BOX_SIZE+1, 1):
                for dx in range(-BOX_SIZE, BOX_SIZE+1, 1):
                    ny,nx = pos.y+dy, pos.x+dx
                    temp = random.randint(MIN_TEMP,MAX_TEMP)
                    temperature[ny][nx] = temp
        return temperature

    # ワームホールと出口セルの対応を予想
    def _predict(self, temperature: List[List[int]]) -> List[int]:
        estimate = [-1] * self.N
        for i_in in range(self.N):
            # you can output comment
            print(f"# measure i={i_in} y=0 x=0")

            measured_value = self.judge.measure(i_in, 0, 0)
            # answer the position with the temperature closest to the measured value
            min_diff = 9999
            for i_out, pos in enumerate(self.exit_pos):
                diff = abs(temperature[pos.y][pos.x] - measured_value)
                if diff < min_diff:
                    min_diff = diff
                    estimate[i_in] = i_out
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
