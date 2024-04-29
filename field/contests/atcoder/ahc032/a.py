from typing import List
import sys
import time
import random

from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport

# 定数
TIME_LIMIT = 1.6
INF = 10**18
MOD = 998244353

class Solver:

    def __init__(self, N: int, M: int, K: int, A: List[List[int]], stamps: List[List[List[int]]]):
        self.N = N # 9
        self.M = M # 20
        self.K = K # 81
        self.A = A
        self.stamps = stamps
        self.start_time = time.time()
        self.current_time = time.time()
        self.best_score = self._calc_score(self.A)
        self.ans = [] # (m,p,q)のリスト

    def solve(self) -> None:
        for _ in range(self.K):
            self.current_time = time.time()
            if self.current_time - self.start_time >= TIME_LIMIT:
                break
            if len(self.ans) >= self.K:
                break

            # 各スタンプを全座標に対し押すシミュレーションをして、最もスコアが伸びるスタンプかつ場所を選ぶ
            m,p,q,m2,p2,q2,m3,p3,q3,m4,p4,q4 = self._greedy_choice2()
            if m != -1 and m2 != -1 and m3 != -1 and len(self.ans)+4 < self.K:
                self.ans.append((m,p,q))
                for dy in range(3):
                    for dx in range(3):
                        self.A[p+dy][q+dx] = (self.A[p+dy][q+dx] + self.stamps[m][dy][dx]) % MOD
                self.ans.append((m2,p2,q2))
                for dy in range(3):
                    for dx in range(3):
                        self.A[p2+dy][q2+dx] = (self.A[p2+dy][q2+dx] + self.stamps[m2][dy][dx]) % MOD
                self.ans.append((m3,p3,q3))
                for dy in range(3):
                    for dx in range(3):
                        self.A[p3+dy][q3+dx] = (self.A[p3+dy][q3+dx] + self.stamps[m3][dy][dx]) % MOD
                self.ans.append((m4,p4,q4))
                for dy in range(3):
                    for dx in range(3):
                        self.A[p4+dy][q4+dx] = (self.A[p4+dy][q4+dx] + self.stamps[m4][dy][dx]) % MOD
            else:
                break
            self.best_score = self._calc_score(self.A)

        # 出力
        print(len(self.ans))
        for m,p,q in self.ans:
            print(m,p,q)

        # スコア出力
        print(len(self.ans), file=sys.stderr)
        print("Score = ",self._calc_score(self.A), file=sys.stderr)

    def _greedy_choice2(self):
        self.current_time = time.time()
        if self.current_time - self.start_time >= TIME_LIMIT:
            return -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1

        best_score = self.best_score
        best_m,best_y,best_x = -1,-1,-1
        cand_A = []
        for m in range(self.M):
            for y in range(self.N-2):
                for x in range(self.N-2):
                    A = [a[:] for a in self.A]
                    for dy in range(3):
                        for dx in range(3):
                            A[y+dy][x+dx] = (A[y+dy][x+dx] + self.stamps[m][dy][dx]) % MOD
                    score = self._calc_score(A)
                    heappush(cand_A,(-score,m,y,x,A))

        self.current_time = time.time()
        if self.current_time - self.start_time >= TIME_LIMIT:
            return -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1

        best_m2,best_y2,best_x2 = -1,-1,-1
        cand_B = []
        for _ in range(50):
            _,m,y,x,A = heappop(cand_A)
            for m2 in range(self.M):
                for y2 in range(self.N-2):
                    for x2 in range(self.N-2):
                        B = [a[:] for a in A]
                        for dy in range(3):
                            for dx in range(3):
                                B[y2+dy][x2+dx] = (B[y2+dy][x2+dx] + self.stamps[m2][dy][dx]) % MOD
                        score = self._calc_score(B)
                        heappush(cand_B,(-score,m,m2,y,x,y2,x2,B))

        self.current_time = time.time()
        if self.current_time - self.start_time >= TIME_LIMIT:
            return -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1

        best_m3,best_y3,best_x3 = -1,-1,-1
        cand_C = []
        for _ in range(40):
            _,m,m2,y,x,y2,x2,B = heappop(cand_B)
            for m3 in range(self.M):
                for y3 in range(self.N-2):
                    for x3 in range(self.N-2):
                        C = [a[:] for a in B]
                        for dy in range(3):
                            for dx in range(3):
                                C[y3+dy][x3+dx] = (C[y3+dy][x3+dx] + self.stamps[m3][dy][dx]) % MOD
                        score = self._calc_score(C)
                        heappush(cand_C,(-score,m,m2,m3,y,x,y2,x2,y3,x3,C))

        self.current_time = time.time()
        if self.current_time - self.start_time >= TIME_LIMIT:
            return -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1

        best_m4,best_y4,best_x4 = -1,-1,-1
        for _ in range(30):
            _,m,m2,m3,y,x,y2,x2,y3,x3,C = heappop(cand_C)
            for m4 in range(self.M):
                for y4 in range(self.N-2):
                    for x4 in range(self.N-2):
                        D = [a[:] for a in C]
                        for dy in range(3):
                            for dx in range(3):
                                D[y4+dy][x4+dx] = (D[y4+dy][x4+dx] + self.stamps[m4][dy][dx]) % MOD
                        score = self._calc_score(D)
                        if score > best_score:
                            best_score = score
                            best_m,best_y,best_x = m,y,x
                            best_m2,best_y2,best_x2 = m2,y2,x2
                            best_m3,best_y3,best_x3 = m3,y3,x3
                            best_m4,best_y4,best_x4 = m4,y4,x4

        return (best_m,best_y,best_x,best_m2,best_y2,best_x2,best_m3,best_y3,best_x3,best_m4,best_y4,best_x4)

    # スコア計算
    def _calc_score(self,A):
        score = 0
        for y in range(self.N):
            for x in range(self.N):
                score += A[y][x] % MOD
        return score

    # 差分スコア計算
    def _calc_score_diff(self,A,m,p,q):
        before_score, after_score = 0,0
        # 変更前スコア計算
        for dy in range(3):
            for dx in range(3):
                before_score += A[p+dy][q+dx] % MOD

        # 変更後スコア計算
        for dy in range(3):
            for dx in range(3):
                after_score += (A[p+dy][q+dx]+self.stamps[m][dy][dx]) % MOD

        return after_score - before_score

def main():
    N,M,K =  map(int,input().split())
    A =  [list(map(int,input().split())) for _ in range(N)]
    stamps = []
    for _ in range(M):
        stamp =  [list(map(int,input().split())) for _ in range(3)]
        stamps.append(stamp)

    solver = Solver(N,M,K,A,stamps)
    solver.solve()

if __name__ == "__main__":
    main()
