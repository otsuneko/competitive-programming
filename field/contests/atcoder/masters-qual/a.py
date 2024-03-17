from dataclasses import dataclass
from typing import List
from heapq import heappush, heappop
from collections import deque
import math
import random
import os
import time
import sys
import copy
input = lambda: sys.stdin.readline().rstrip()

### CONST ###
INF = 10**18
TIME_LIMIT = 1
MOVE = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIR = {"U":(-1,0), "R":(0,1), "D":(1,0), "L":(0,-1)}
INV_DIR = {(-1,0):"U", (0,1):"R", (1,0):"D", (0,-1):"L"}
VIS_FLG = True # visualize用のテキストを吐き出すかどうか
# VIS_FLG = False

### Class ###
if VIS_FLG:
    class Visualizer():
        """ビジュアライズ用クラス
        Note:
            出力ファイルのハンドル
            描画コマンドのファイル出力用関数の提供
        """
        def __init__(self):
            # 描画コマンド出力用ファイルのopen
            output_file_path = os.getcwd() + '/../visualizer/VisCommands.txt'
            self.f = open(output_file_path, 'w')

        ### 描画コマンド呼び出し ###
        def turn(self, t):
            self.f.write("time = {};\n".format(t))

        def always(self):
            self.turn(-1)

        def arc(self, x, y, w, h, start, stop):
            self.f.write("arc( {}, {}, {}, {}, {}, {});\n".format(x, y, w, h, start, stop))

        def ellipse(self, x, y, w, h):
            self.f.write("ellipse( {}, {}, {}, {});\n".format(x, y, w, h))

        def circle(self, x, y, d):
            self.f.write("circle( {}, {}, {});\n".format(x, y, d))

        def line(self, x1, y1, x2, y2):
            self.f.write("line( {}, {}, {}, {});\n".format(x1, y1, x2, y2))

        def point(self, x, y):
            self.f.write("point( {}, {});\n".format(x, y))

        def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
            self.f.write("quad( {}, {}, {}, {}, {}, {}, {}, {});\n".format(x1, y1, x2, y2, x3, y3, x4, y4))

        def rect(self, x, y, w, h):
            self.f.write("rect( {}, {}, {}, {});\n".format(x, y, w, h))

        def square(self, x, y, s):
            self.f.write("square( {}, {}, {});\n".format(x, y, s))

        def triangle(self, x1, y1, x2, y2, x3, y3):
            self.f.write("triangle( {}, {}, {}, {}, {}, {});\n".format(x1, y1, x2, y2, x3, y3))

        def background(self, r, g, b):
            self.f.write("background({},{},{});\n".format(r, g, b))

        def clear(self):
            self.f.write("clear();\n")

        def color_mode(self, mode, max1, max2, max3, maxA):
            self.f.write("colorMode({}, {}, {}, {}, {});\n".format(mode, max1, max2, max3, maxA))

        def fill(self, r, g, b, a):
            self.f.write("fill({}, {}, {}, {});\n".format(r, g, b, a))

        def no_fill(self):
            self.f.write("noFill();\n")

        def no_stroke(self):
            self.f.write("noStroke();\n")

        def stroke(self, r, g, b, a):
            self.f.write("stroke({}, {}, {}, {});\n".format(r, g, b, a))

        def erase(self):
            self.f.write("erase();\n")

        def no_erase(self):
            self.f.write("noErase();\n")

        def text_align(self, alignX, alignY):
            self.f.write("textAlign({}, {});\n".format(alignX, alignY))

        def text_leading(self, leading):
            self.f.write("textLeading({});\n".format(leading))

        def text_size(self, size):
            self.f.write("textSize({});\n".format(size))

        def text_style(self, style):
            self.f.write("textStyle({});\n".format(style))

        def text_width(self, text):
            self.f.write("textWidth({});\n".format(text))

        def text_ascent(self):
            self.f.write("textAscent();\n")

        def text_descent(self):
            self.f.write("textDescent();\n")

        def text_wrap(self, wrap):
            self.f.write("textWrap({});\n".format(wrap))

        def text(self, text, x, y):
            self.f.write("text(\"{}\", {}, {});\n".format(text, x, y))

class Coord:
    """座標クラス
    Note:
        各油田が持つマス数とその座標を持つ
    Attributes
        y (int): y座標(縦方向下向き)
        x (int): x座標(横方向右向き)
    """
    y: int
    x: int

    def __init__(self,y,x):
        self.y = y
        self.x = x

class Solver:
    """ソルバクラス
    Note:
        解法を記載するクラス
    Attributes

    """
    def __init__(self,t,n,wall_v,wall_h,A):
        self.start_time = time.time()
        self.current_time = time.time()
        self.t = t
        self.N = n
        self.wall_v = wall_v
        self.wall_h = wall_h
        self.A = A

        if VIS_FLG:
            self.vis = Visualizer()

        self.turn = 0
        self.turn_limit = 4*n*n
        self.cost = 0
        self.max_score = 0
        self.ini_squared_sum = self.calc_squared_sum() # 初期時点での隣接マスの数字の差の二乗和
        self.ans = [] # (交換するか, 高橋くんの移動方向、青木くんの移動方向、高橋くんの移動先座標、青木くんの移動先座標)
        self.visit_count = [[0]*2 for _ in range(2)] # グリッドを4分割した領域の訪問数をカウント

        # 高橋くん青木くんの座標
        self.t_pos = Coord(0,0)
        self.a_pos = Coord(0,0)
        self.ini_t_pos = Coord(0,0)
        self.ini_a_pos = Coord(0,0)
        self.moved_flg = False

    ### ここに解法を記載 ###
    def solve(self):

        # 高橋くんと青木くんの初期位置をランダムに決定
        while 1:
            self.t_pos = Coord(random.randint(0,self.N-1), random.randint(0,self.N-1))
            self.a_pos = Coord(random.randint(0,self.N-1), random.randint(0,self.N-1))
            if abs(self.t_pos.y - self.a_pos.y) + abs(self.t_pos.x - self.a_pos.x) >= self.N*1.5:
                self.ini_t_pos = copy.deepcopy(self.t_pos)
                self.ini_a_pos = copy.deepcopy(self.a_pos)
                break
        self.visit_count[self.t_pos.y > self.N//2][self.t_pos.x > self.N//2] += 1
        self.visit_count[self.a_pos.y > self.N//2][self.a_pos.x > self.N//2] += 1
        self.ans.append((self.t_pos,self.a_pos))

        # ターンいっぱいランダム移動と交換をスコアが上がる限り繰り返す
        while self.turn < self.turn_limit:
            # TLE対策
            self.current_time = time.time()
            if self.current_time - self.start_time >= TIME_LIMIT:
                break

            if self.turn < self.turn_limit // 2:
                # 交換するかどうかの決定
                switch = 0 # デフォは交換しない
                # 交換してスコアが上がるかを計算
                diff = self.calc_diff_squared_sum()
                if diff < 0:
                    switch = 1
                    # 実際に数字を交換
                    self.A[self.t_pos.y][self.t_pos.x], self.A[self.a_pos.y][self.a_pos.x] = self.A[self.a_pos.y][self.a_pos.x], self.A[self.t_pos.y][self.t_pos.x]
                else:
                    # 交換しない
                    switch = 0

                # 移動先の決定
                nxt_t = "."
                nxt_a = "."
                while (nxt_t == "." and nxt_a == "."):
                    # 高橋くんの移動先
                    t_dir = random.choice(["U","R","D","L"])
                    dy,dx = DIR[t_dir]
                    ny,nx = self.t_pos.y+dy,self.t_pos.x+dx
                    # 範囲外に出ず、壁が無いことが移動できる条件
                    if self.is_movable(self.t_pos.y, self.t_pos.x, dy,dx):
                        nxt_t = t_dir
                        self.t_pos = Coord(ny,nx)

                    # 青木くんの移動先
                    a_dir = random.choice(["U","R","D","L"])
                    dy,dx = DIR[a_dir]
                    ny,nx = self.a_pos.y+dy,self.a_pos.x+dx
                    # 範囲外に出ず、壁が無いことが移動できる条件
                    if self.is_movable(self.a_pos.y, self.a_pos.x, dy,dx):
                        nxt_a = a_dir
                        self.a_pos = Coord(ny,nx)

                # 4分割したエリアの訪問数をプラス
                self.visit_count[self.t_pos.y > self.N//2][self.t_pos.x > self.N//2] += 1
                self.visit_count[self.a_pos.y > self.N//2][self.a_pos.x > self.N//2] += 1
                self.ans.append((switch, nxt_t, nxt_a, self.t_pos, self.a_pos))
                self.turn += 1

            # 後半戦に差し掛かった時点で高橋くんを大移動する
            else:
                if self.moved_flg == False:
                    min_id = [0,0]
                    min_cnt = INF
                    for y in range(2):
                        for x in range(2):
                            if self.visit_count[y][x] < min_cnt:
                                min_cnt = self.visit_count[y][x]
                                min_id = [0,0]

                    dest_y,dest_x = self.N//2 + self.N * min_id[0], self.N//2 + self.N * min_id[1]
                    # BFSで最短経路を計算
                    dirs_t = self.bfs(self.t_pos.y,self.t_pos.x,dest_y,dest_x)
                    dirs_a = self.bfs(self.a_pos.y,self.a_pos.x,dest_y,dest_x)
                    if len(dirs_t) > len(dirs_a):
                        # 高橋くんを大移動
                        while dirs_t and self.turn < self.turn_limit:

                            # 交換するかどうかの決定
                            switch = 0 # デフォは交換しない
                            # 交換してスコアが上がるかを計算
                            diff = self.calc_diff_squared_sum()
                            if diff < 0:
                                switch = 1
                                # 実際に数字を交換
                                self.A[self.t_pos.y][self.t_pos.x], self.A[self.a_pos.y][self.a_pos.x] = self.A[self.a_pos.y][self.a_pos.x], self.A[self.t_pos.y][self.t_pos.x]
                            else:
                                # 交換しない
                                switch = 0

                            # 移動先の決定
                            # 高橋くんは固定
                            nxt_t = dirs_t[0]
                            dy,dx = DIR[nxt_t]
                            self.t_pos = Coord(self.t_pos.y+dy, self.t_pos.x+dx)
                            dirs_t.pop(0)

                            nxt_a = "."
                            # 青木くんの移動先
                            a_dir = random.choice(["U","R","D","L"])
                            dy,dx = DIR[a_dir]
                            ny,nx = self.a_pos.y+dy,self.a_pos.x+dx
                            # 範囲外に出ず、壁が無いことが移動できる条件
                            if self.is_movable(self.a_pos.y, self.a_pos.x, dy,dx):
                                nxt_a = a_dir
                                self.a_pos = Coord(ny,nx)

                            self.ans.append((switch, nxt_t, nxt_a, self.t_pos, self.a_pos))
                            self.turn += 1
                    else:
                        # 青木くんを大移動
                        while dirs_a and self.turn < self.turn_limit:
                            # 交換するかどうかの決定
                            switch = 0 # デフォは交換しない
                            # 交換してスコアが上がるかを計算
                            diff = self.calc_diff_squared_sum()
                            if diff < 0:
                                switch = 1
                                # 実際に数字を交換
                                self.A[self.t_pos.y][self.t_pos.x], self.A[self.a_pos.y][self.a_pos.x] = self.A[self.a_pos.y][self.a_pos.x], self.A[self.t_pos.y][self.t_pos.x]
                            else:
                                # 交換しない
                                switch = 0

                            # 移動先の決定
                            # 青木くんは固定
                            nxt_a = dirs_a[0]
                            dy,dx = DIR[nxt_a]
                            self.a_pos = Coord(self.a_pos.y+dy, self.a_pos.x+dx)
                            dirs_a.pop(0)

                            nxt_t = "."
                            # 高橋くんの移動先
                            t_dir = random.choice(["U","R","D","L"])
                            dy,dx = DIR[t_dir]
                            ny,nx = self.t_pos.y+dy,self.t_pos.x+dx
                            # 範囲外に出ず、壁が無いことが移動できる条件
                            if self.is_movable(self.t_pos.y, self.t_pos.x, dy,dx):
                                nxt_t = t_dir
                                self.t_pos = Coord(ny,nx)

                            self.ans.append((switch, nxt_t, nxt_a, self.t_pos, self.a_pos))
                            self.turn += 1

                    self.moved_flg = True

                # 交換するかどうかの決定
                switch = 0 # デフォは交換しない
                # 交換してスコアが上がるかを計算
                diff = self.calc_diff_squared_sum()
                if diff < 0:
                    switch = 1
                    # 実際に数字を交換
                    self.A[self.t_pos.y][self.t_pos.x], self.A[self.a_pos.y][self.a_pos.x] = self.A[self.a_pos.y][self.a_pos.x], self.A[self.t_pos.y][self.t_pos.x]
                else:
                    # 交換しない
                    switch = 0

                # 移動先の決定
                nxt_t = "."
                nxt_a = "."
                # 高橋くんの移動先
                t_dir = random.choice(["U","R","D","L"])
                dy,dx = DIR[t_dir]
                ny,nx = self.t_pos.y+dy,self.t_pos.x+dx
                # 範囲外に出ず、壁が無いことが移動できる条件
                if self.is_movable(self.t_pos.y, self.t_pos.x, dy,dx):
                    nxt_t = t_dir
                    self.t_pos = Coord(ny,nx)

                # 青木くんの移動先
                a_dir = random.choice(["U","R","D","L"])
                dy,dx = DIR[a_dir]
                ny,nx = self.a_pos.y+dy,self.a_pos.x+dx
                # 範囲外に出ず、壁が無いことが移動できる条件
                if self.is_movable(self.a_pos.y, self.a_pos.x, dy,dx):
                    nxt_a = a_dir
                    self.a_pos = Coord(ny,nx)

                # 4分割したエリアの訪問数をプラス
                self.visit_count[self.t_pos.y > self.N//2][self.t_pos.x > self.N//2] += 1
                self.visit_count[self.a_pos.y > self.N//2][self.a_pos.x > self.N//2] += 1
                self.ans.append((switch, nxt_t, nxt_a, self.t_pos, self.a_pos))
                self.turn += 1

        # 最終結果を回答
        t_pos,a_pos = self.ans[0]
        print(t_pos.y,t_pos.x,a_pos.y,a_pos.x)
        for t in range(1,len(self.ans)):
            print(*self.ans[t][:3])

        if VIS_FLG:
            self.visualize()

    def bfs(self,sy,sx,gy,gx):
        queue = deque([[sy,sx,[]]])
        visited = [[-1]*self.N for _ in range(self.N)]
        visited[sy][sx] = 0
        while queue:
            y,x,dirs = queue.popleft()
            if [y,x] == [gy,gx]:
                return dirs
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if self.is_movable(y,x,dy,dx) and visited[ny][nx] == -1:
                    visited[ny][nx] = visited[y][x] + 1
                    queue.append([ny, nx, dirs + [INV_DIR[(dy,dx)]]])


    # その方向に進めるかどうかの判定
    def is_movable(self,y,x,dy,dx):


        ny,nx = y+dy, x+dx

        # グリッドの範囲内に収まっているか
        if not (0<=ny<self.N and 0<=nx<self.N):
            return False

        # 進もうとしている方向に水路が無いか
        # 下に進む場合
        if [dy,dx] == [1,0] and self.wall_h[y][x] == "1":
            return False
        # 上に進む場合
        elif [dy,dx] == [-1, 0] and self.wall_h[y-1][x] == "1":
            return False
        # 右に進む場合
        elif [dy,dx] == [0, 1] and self.wall_v[y][x] == "1":
            return False
        # 左に進む場合
        elif [dy,dx] == [0, -1] and self.wall_v[y][x-1] == "1":
            return False

        return True

    def calc_diff_squared_sum(self):
        """数字を交換した時の隣接セルの差の二乗和が減るか増えるかを計算
        """
        # 交換前の二人の座標の隣接セルの差の二乗和を計算
        before_sum = 0
        for dy,dx in MOVE:
            # 高橋くん
            ny,nx = self.t_pos.y+dy,self.t_pos.x+dx
            if self.is_movable(self.t_pos.y,self.t_pos.x,dy,dx):
                before_sum += (self.A[self.t_pos.y][self.t_pos.x] - self.A[ny][nx])**2
            # 青木くん
            ny,nx = self.a_pos.y+dy,self.a_pos.x+dx
            if self.is_movable(self.a_pos.y,self.a_pos.x,dy,dx):
                before_sum += (self.A[self.a_pos.y][self.a_pos.x] - self.A[ny][nx])**2

        # 2点の数字を交換
        self.A[self.t_pos.y][self.t_pos.x], self.A[self.a_pos.y][self.a_pos.x] = self.A[self.a_pos.y][self.a_pos.x], self.A[self.t_pos.y][self.t_pos.x]

        # 交換後の二人の座標の隣接セルの差の二乗和を計算
        after_sum = 0
        for dy,dx in MOVE:
            # 高橋くん
            ny,nx = self.t_pos.y+dy,self.t_pos.x+dx
            if self.is_movable(self.t_pos.y,self.t_pos.x,dy,dx):
                after_sum += (self.A[self.t_pos.y][self.t_pos.x] - self.A[ny][nx])**2
            # 青木くん
            ny,nx = self.a_pos.y+dy,self.a_pos.x+dx
            if self.is_movable(self.a_pos.y,self.a_pos.x,dy,dx):
                after_sum += (self.A[self.a_pos.y][self.a_pos.x] - self.A[ny][nx])**2

        # 後始末(2点の数字を交換して元に戻す)
        self.A[self.t_pos.y][self.t_pos.x], self.A[self.a_pos.y][self.a_pos.x] = self.A[self.a_pos.y][self.a_pos.x], self.A[self.t_pos.y][self.t_pos.x]

        return after_sum - before_sum


    def calc_squared_sum(self) -> int:
        """隣接するマスのペア全体の集合を E とし、隣接マスの数字の差の二乗和を計算
        """
        su = 0
        for y in range(self.N):
            for x in range(self.N):
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    # 範囲外に出ず、壁が無いことが移動できる条件
                    if self.is_movable(y,x,dy,dx):
                            su += (self.A[y][x] - self.A[ny][nx])**2

        return su

    def calc_score(self,squared_sum) -> int:
        """現時点の隣接マスの数字の差の二乗和を基に計算したスコア
        """
        score = max(1, round(10**6 * math.log2(self.ini_squared_sum) / squared_sum))
        return score

    def visualize(self):
        """診断人さんのビジュアライザに食わせるテキストファイルに描画コマンドを出力
           まずは全ターン常に表示する要素を出力し、その後ターン別の要素を出力(インタラクティブ問の場合は出力の度に出力する)
        """

        self.vis.always()

        # 迷路の壁を描画
        sz = 20 # ビジュアライズする時の視認性を調整するピクセル倍率
        self.vis.stroke(0, 0, 0, 255)
        self.vis.no_fill()
        self.vis.rect(0, 0, sz * self.N, sz * self.N)
        self.vis.fill(255, 255, 255, 255)

        for y in range(self.N):
            for x in range(self.N - 1):
                if self.wall_v[y][x] == "1":
                    self.vis.line(x * sz+sz, y * sz, x * sz+sz, (y + 1) * sz)

        for y in range(self.N - 1):
            for x in range(self.N):
                if self.wall_h[y][x] == "1":
                    self.vis.line(x * sz, y * sz+sz, (x + 1) * sz, y * sz+sz)

        # 各セルに書かれた数字を描画
        for y in range(self.N):
            for x in range(self.N):
                self.vis.text_size(10) #文字サイズはszに合わせる
                self.vis.stroke(0, 0, 0, 255)
                self.vis.text(self.A[y][x],x*sz,y*sz+sz)

        # 初期位置の描画
        # t_pos,a_pos = self.ans[0]
        # self.vis.no_stroke()
        # self.vis.square(t_pos.x*sz, t_pos.y*sz, sz)
        # self.vis.fill(255, 200, 200, 200)
        # self.vis.no_stroke()
        # self.vis.square(a_pos.x*sz, a_pos.y*sz, sz)
        # self.vis.fill(200, 200, 255, 200)

        # 毎ターンの動きの描画
        for t in range(1, len(self.ans)):
            self.vis.turn(t)

            s,d,e,t_pos,a_pos = self.ans[t]
            self.vis.text_size(sz) #文字サイズはszに合わせる
            self.vis.no_stroke()
            self.vis.square(t_pos.x*sz, t_pos.y*sz, sz)
            self.vis.fill(255, 200, 200, 200)

            self.vis.no_stroke()
            self.vis.square(a_pos.x*sz, a_pos.y*sz, sz)
            self.vis.fill(200, 200, 255, 200)

            # 各セルに書かれた数字を描画
            for y in range(self.N):
                for x in range(self.N):
                    self.vis.text_size(10) #文字サイズはszに合わせる
                    self.vis.stroke(0, 0, 0, 255)
                    self.vis.text(self.A[y][x],x*sz,y*sz+sz)

### メイン関数 ###
def main():
    t,N = map(int, input().split())
    wall_v = [list(input()) for _ in range(N)] # 壁が縦にある場合(横移動可否判定)
    wall_h = [list(input()) for _ in range(N-1)] # 壁が横にある場合(縦移動可否判定)
    A = [list(map(int,input().split())) for _ in range(N)]

    solver = Solver(t,N,wall_v,wall_h,A)
    solver.solve()

if __name__ == "__main__":
    main()


### ここからはAHCでよく使うスニペットたち ###

### グリッド上の壁の入力と移動可否判定 ###
# wall_v = [list(input()) for _ in range(H-1)]
# wall_h = [list(input()) for _ in range(H)]

# y,x = 0,0
# for dy,dx in MOVE:
#     ny,nx = y+dy,x+dx
#     # 範囲外に出ず、壁が無いことが移動できる条件
#     if 0<=ny<H and 0<=nx<W:
#         if dy == 0 and wall_h[y][min(x,nx)] == "0" or dx == 0 and wall_v[min(y,ny)][x] == "0":
