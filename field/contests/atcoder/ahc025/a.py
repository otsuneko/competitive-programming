from typing import List
import sys
import time
import random

# 定数
TIME_LIMIT = 2.0
INI_WEIGHT = 5000
INF = 10**18

class Judge:

    # 天秤で重さを測る
    def measure(self, nl:int, nr:int, L:List[int], R:List[int]) -> str:
        print(nl,nr,*L,*R, flush=True)
        res = input()
        return res

    # D個の集合に分割したアイテムを回答
    def answer(self, estimate: List[int]) -> None:
        print(*estimate)
        sys.stdout.flush()

class Solver:

    def __init__(self, N: int, D: int, Q: int):
        self.N = N
        self.D = D
        self.Q = Q
        self.judge = Judge()

        self.weights = [INI_WEIGHT]*N

    def solve(self) -> None:
        for _ in range(self.Q):
            nl,nr,L,R = self.decide_measure_target()
            self.judge.measure(nl,nr,L,R)
        estimate = self.estimate_answer()
        self.judge.answer(estimate)

    # 次の測定対象を決める
    def decide_measure_target(self):
        L,R = [],[]
        return len(L),len(R),L,R

    # 焼きなましでちょうどいいグループ分割を探索
    def estimate_answer(self):
        estimate = [-1] * self.N
        return estimate


def main():
    N, D, Q = map(int,input().split())
    solver = Solver(N,D,Q)
    solver.solve()


if __name__ == "__main__":
    main()
