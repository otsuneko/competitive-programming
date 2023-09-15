from typing import List
import sys
import time
import random
from collections import deque

# 定数
TIME_LIMIT = 2.0
INF = 10**18
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])

class Solver:

    def __init__(self, T, H, W, y_exit, water_h, water_w, K, crops):
        self.start = time.time()
        self.T = T
        self.H = H
        self.W = W
        self.y_exit = y_exit
        self.water_h = water_h
        self.water_w = water_w
        self.K = K
        self.crops = crops

        # 栽培する作物を第1キー：収穫時期の早い順、第2キー：栽培開始時期の早い順でソート
        self.crops.sort(key=lambda x:(x[2],x[1]))
        # print(*self.crops, sep="\n", file=sys.stderr)

    def solve(self):
        # BFSでグリッドの到達可能地点とその距離を計算
        dists = self.calc_move_dist()
        # print(*dists, sep="\n", file=sys.stderr)

        # 栽培計画を作成
        crops_order = self.create_cultivate_plan(dists)

        # 出力
        M = len(crops_order)
        print(M)
        for i in range(M):
            print(*crops_order[i])

    # グリッドの到達可能地点及び最短距離を計算
    def calc_move_dist(self):            
        # BFSで最短距離を計算
        queue = deque([[self.y_exit, 0]])
        dists = [[-1] * self.W for _ in range(self.H)]
        dists[self.y_exit][0] = 0
        while queue:
            y,x = queue.popleft()
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if self.is_movable(y,x,dy,dx) and dists[ny][nx] == -1:
                    dists[ny][nx] = dists[y][x] + 1
                    queue.append([ny, nx])
        
        return dists

    # その方向に進めるかどうかの判定
    def is_movable(self,y,x,dy,dx):
        ny,nx = y+dy, x+dx
        
        # グリッドの範囲内に収まっているか
        if not (0<=ny<self.H and 0<=nx<self.W):
            return False

        # 進もうとしている方向に水路が無いか
        # 下に進む場合
        if [dy,dx] == [1,0] and self.water_h[y][x] == "1":
            return False
        # 上に進む場合
        elif [dy,dx] == [-1, 0] and self.water_h[y-1][x] == "1":
            return False
        # 右に進む場合
        elif [dy,dx] == [0, 1] and self.water_w[y][x] == "1":
            return False
        # 左に進む場合
        elif [dy,dx] == [0, -1] and self.water_w[y][x-1] == "1":
            return False

        return True
    
    # 作物の栽培&収穫計画を作成
    def create_cultivate_plan(self, dists):
        crops_order = [] # 栽培する作物のID、座標、何ヶ月目に植えるかの情報

        # 一旦植えた全ての作物を収穫してまた植えるのをTヶ月経過するまで3回繰り返す
        month = 1
        crop_idx = 0
        while len(crops_order) < self.K:
            # グリッドが埋まるまで奥から順番に収穫時期が遅い作物を植えていく
            # 実際にはグリッドの入り口近くの方から収穫時期が早い作物を奥に向かって詰めていくイメージ。
            # 栽培開始時期より早く植えても問題はないため、栽培開始できる最初の月に全部植えるのを繰り返す。

            # BFSで最短距離を計算
            queue = deque([[self.y_exit, 0]])
            cropped = [[False] * self.W for _ in range(self.H)]
            latest_harvest_month = 1
            while queue:
                y,x = queue.popleft()
                # print(y,x,file=sys.stderr)
                # そのmonthで栽培開始可能　かつ　植える価値の高い作物を植える
                # TODO:つまり、D-Sが小さい(栽培開始時期が遅い)作物は後回しにする。
                while 1:
                    if crop_idx >= self.K:
                        return crops_order
                    
                    # 今見ている作物の栽培開始時期が現在の月以降の場合だけ栽培可能
                    if self.crops[crop_idx][1] < month:
                        crop_idx += 1
                        continue

                    # TODO: うまみが少ない作物は植えずにスキップさせているが、後回しにして植えるでもいいはず
                    if self.crops[crop_idx][2] - self.crops[crop_idx][1] <= 5:
                        crop_idx += 1
                        continue

                    cropped[y][x] = True
                    crops_order.append((self.crops[crop_idx][0], y, x, month))
                    latest_harvest_month = max(latest_harvest_month, self.crops[crop_idx][2])
                    crop_idx += 1
                    break

                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if self.is_movable(y,x,dy,dx) and cropped[ny][nx] == False:
                        cropped[ny][nx] = True
                        queue.append([ny, nx])
            
            month = max(month, latest_harvest_month+1)

        # print(crops_order,file=sys.stderr)
        return crops_order

def main():
    # T = 100, H = W = 20, y_exitは出口のある最左壁のy座標
    T, H, W, y_exit = map(int,input().split())
    water_h = [list(input()) for _ in range(H-1)]
    water_w = [list(input()) for _ in range(H)]

    # K個の作物の栽培開始時期と収穫時期
    K = int(input())
    crops = []
    for i in range(1,K+1):
        S,D = map(int,input().split())
        crops.append((i,S,D))

    solver = Solver(T, H, W, y_exit, water_h, water_w, K, crops)
    solver.solve()

if __name__ == "__main__":
    main()
