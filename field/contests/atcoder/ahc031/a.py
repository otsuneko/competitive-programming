from dataclasses import dataclass
from typing import List
from heapq import heappush, heappop
from collections import deque
import math
import random
import time
import sys,pypyjit
input = lambda: sys.stdin.readline().rstrip()
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

### CONST ###
INF = 10**18
TIME_LIMIT = 2.85
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
MOVE_AROUND = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動

@dataclass
class Rect:
    x1: int
    y1: int
    x2: int
    y2: int
    area: int

class Solver:
    """ソルバクラス
    Note:
        解法を記載するクラス
    Attributes
    """
    def __init__(self, w: int, d: int, n: int, req_areas: List[List[int]]):
        self.start_time = time.time()
        self.current_time = time.time()
        self.W= w
        self.D = d
        self.N = n
        self.req_areas = req_areas

    def solve(self):

        ans = []

        # Nの値によって区画の大きさを変更する
        block_num = 10
        block_len = self.W // block_num
        if self.N > 10:
            block_num = 50
            block_len = self.W // block_num

        # D日分の処理
        for d in range(self.D):
            rects = []
            used_pos = [[0]*block_num for _ in range(block_num)]
            print(self.req_areas[d],file=sys.stderr)
            for n in range(self.N-1,-1,-1):
                max_bx1,max_by1,max_bx2,max_by2,max_area = 0,0,0,0,0
                min_cover_ratio = 10.0**18
                for by1 in range(block_num):
                    for bx1 in range(block_num):
                        if used_pos[by1][bx1]:
                            continue
                        for by2 in range(by1+1,block_num+1):
                            for bx2 in range(bx1+1,block_num+1):
                                area = (bx2-bx1)*(by2-by1)*block_len*block_len
                                cover_ratio = area / self.req_areas[d][n]
                                if area >= self.req_areas[d][n] and cover_ratio <= min_cover_ratio and not self.is_overlap(block_len * bx1, block_len * by1, block_len * bx2, block_len * by2, rects):
                                    max_area = area
                                    min_cover_ratio = cover_ratio
                                    max_bx1,max_by1,max_bx2,max_by2 = bx1,by1,bx2,by2

                if max_area == 0:
                    for by1 in range(block_num):
                        for bx1 in range(block_num):
                            if used_pos[by1][bx1]:
                                continue
                            for by2 in range(by1+1,block_num+1):
                                for bx2 in range(bx1+1,block_num+1):
                                    area = (bx2-bx1)*(by2-by1)*block_len*block_len
                                    if not self.is_overlap(block_len * bx1, block_len * by1, block_len * bx2, block_len * by2, rects):
                                        max_area = area
                                        max_bx1,max_by1,max_bx2,max_by2 = bx1,by1,bx2,by2
                                        break
                                else:
                                    continue
                                break
                            else:
                                continue
                            break
                        else:
                            continue
                        break

                rects.append(Rect(block_len * max_bx1, block_len * max_by1, block_len * max_bx2, block_len * max_by2, max_area))
                for by in range(max_by1,max_by2):
                    for bx in range(max_bx1,max_bx2):
                        used_pos[by][bx] = 1

                if d == 3:
                    print(d,n,file=sys.stderr)
                    for y in range(block_num):
                        print(*used_pos[y],file=sys.stderr)


            rects = rects[::-1]
            ans.append(rects)

        for d in range(self.D):
            for n in range(self.N):
                print(ans[d][n].y1, ans[d][n].x1, ans[d][n].y2, ans[d][n].x2)

    def is_overlap(self, x1, y1, x2, y2, rects):
        for rect in rects:
            x3,y3,x4,y4 = rect.x1,rect.y1,rect.x2,rect.y2
            if max(x1,x3) < min(x2,x4) and max(y1,y3) < min(y2,y4):
                return True
        return False

def main():
    W,D,N = map(int, input().split())
    req_areas =  [list(map(int,input().split())) for _ in range(D)]

    solver = Solver(W,D,N,req_areas)
    solver.solve()

if __name__ == "__main__":
    main()
