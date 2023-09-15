import sys
import time
import random
from collections import deque
from collections import defaultdict
from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport
sys.setrecursionlimit(10**7)
            
# 定数
TIME_LIMIT = 3.0
INF = 10**18
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1]) #縦横
MIN_SD_SPAN = 8 # D-Sがこの値以下の作物はうまみが少ないとしてスキップ
LIMIT_END_MONTH = 90 # MIN_SD_SPANを無くす月

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1]*n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def size(self, x):
        return -self.parents[self.find(x)]

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return len(self.roots())

    def all_group_members(self):
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find(member)].append(member)
        return group_members

    def __str__(self):
        return '\n'.join(f'{r}: {m}' for r, m in self.all_group_members().items())


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
        self.crops = deque(self.crops)
        # print(*self.crops, sep="\n", file=sys.stderr)

        # グリッド上の各座標で作物が植えられているかどうか
        # [その座標に作物が植えられているか, 作物のID, 栽培開始時期S, 収穫時期D]
        self.grid_status = [[{"flg":False, "idx":-1, "S":-1, "D":-1} for _ in range(self.W)] for _ in range(self.H)]

    def solve(self):
        # 栽培計画を作成
        crops_order = self.create_cultivate_plan()

        # 出力
        M = len(crops_order)
        print(M)
        for i in range(M):
            print(*crops_order[i])

    # グリッドの到達可能地点及び最短距離を計算
    def calc_move_dist(self):

        # 壁際の方が距離が遠い扱いになるように補正
        additional_dists = [[0] * self.W for _ in range(self.H)]
        for y in range(self.H):
            for x in range(self.W):
                for dy,dx in MOVE:
                    if not self.is_movable(y,x,dy,dx):
                        additional_dists[y][x] += 0.1

        # BFSで最短距離を計算
        queue = deque([[self.y_exit, 0]])
        dists = [[-1] * self.W for _ in range(self.H)]
        dists[self.y_exit][0] = 0
        cultivatable_pos = set() # 栽培可能な座標と、その座標の入り口からの距離
        while queue:
            y,x = queue.popleft()
            cultivatable_pos.add((dists[y][x],y,x))
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if self.is_movable(y,x,dy,dx) and self.grid_status[ny][nx]["flg"] == False and dists[ny][nx] == -1:
                    dists[ny][nx] = dists[y][x] + additional_dists[ny][nx] + 1
                    # dists[ny][nx] = dists[y][x] + 1
                    queue.append([ny, nx])
        
        return dists, cultivatable_pos

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
    def create_cultivate_plan(self):
        crops_order = [] # 栽培する作物のID、座標、何ヶ月目に植えるかの情報
        # BFSでグリッドの到達可能地点とその距離を計算
        dists, cultivatable_pos = self.calc_move_dist()
        sorted_cultivatable_pos = self.cultivatable_pos_sort(cultivatable_pos, dists)

        # フェーズ1：初月の栽培
        # グリッドの入り口から順に収穫時期が早い作物を奥に向かって詰めていく。
        # 栽培開始時期より早く植えても問題はないため、最初の月に植えられるだけ植える。
        # TODO: 初月に全部を貪欲に植えるのが本当に良いのかは調査が必要。乱数でシミュレーションする？

        # 未栽培のマスだけを通ってたどり着ける栽培済マスの入次数
        indeg_crops = defaultdict(int)
        
        # 各未栽培マスへの入次数をBFSで計算
        indeg_uncrops = self.calc_indeg_uncrops(cultivatable_pos, dists)        

        # 収穫時期が早い作物を400個選んで並び替えることで埋め尽くす
        ini_crops = []
        for i,s,d in self.crops:
            if len(ini_crops) == self.H * self.W:
                break
            if d - s <= MIN_SD_SPAN:
                continue
            ini_crops.append((i,s,d))
        ini_crops = ini_crops[::-1]

        month = 1
        uf = UnionFind(self.H*self.W)
        cropped = set()
        for dist,y,x in sorted_cultivatable_pos:
            # そのmonthに栽培開始可能　かつ　植える価値の高い作物を植える
            # TODO:つまり、D-Sが小さい(栽培開始時期が遅い)作物は後回しにする。
            for i in range(len(ini_crops)):
                crop_idx, s, d = ini_crops[i]

                # 今見ている作物の栽培開始時期Sが現在の月以降の場合だけ栽培可能
                if s < month:
                    continue

                if (crop_idx,s,d) in cropped:
                    continue

                # TODO: うまみが少ない作物は植えずにスキップさせているが、後回しにして植えるでもいいはず
                # 乱数で植えるパターン植えないパターンを試して一番スコアいいヤツにする？
                if d - s <= MIN_SD_SPAN:
                    continue

                # 追加栽培予定マスが道を塞ぐ場合はスキップ
                if not self.is_cultivatable(y,x,uf,dists, indeg_crops,d,indeg_uncrops):
                    continue

                # 植える
                self.grid_status[y][x] = {"flg":True, "idx":crop_idx, "S":s, "D":d}
                crops_order.append((crop_idx, y, x, month))
                self.crops.remove((crop_idx, s, d))
                cropped.add((crop_idx, s, d))

                # 今回植えた作物の収穫時期が隣接する作物と同じならUnionFindの同グループ化
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if self.is_movable(y,x,dy,dx) and self.grid_status[ny][nx]["flg"] == True:
                        if self.grid_status[ny][nx]["D"] == d:
                            uf.union(y*self.H + x, ny*self.H + nx)

                # 今回植えた作物によって塞がれた隣接マスの入次数減と、今回植えた作物の入次数カウント
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if self.is_movable(y,x,dy,dx):
                        # 隣が作物ならその作物へ至る経路を1つ塞いだことになる
                        if self.grid_status[ny][nx]["flg"] == True:
                            indeg_crops[uf.find(ny*self.W + nx)] -= 1
                        else:
                            # 隣が通行可能かつより入り口に近いなら自分のマスへ至る道が1つあることになる
                            if dists[ny][nx] < dists[y][x]:
                                indeg_crops[uf.find(y*self.W + nx)] += 1
                            # 隣が通行可能かつより入り口から遠いなら、そのマスへ至る道を1つ塞いだことになる
                            elif dists[ny][nx] > dists[y][x]:
                                indeg_uncrops[ny][nx] -= 1

                break

        # DFSの帰りがけカウントで、通路を埋めてもいい最小のDを求める
        seen = set()
        min_allowed_D = defaultdict(int)
        def calc_min_allowed_D(y,x):
            seen.add((y,x))
            mi = INF
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if self.is_movable(y,x,dy,dx):
                    # 未到達で未栽培なら探索継続
                    if (ny,nx) not in seen and self.grid_status[ny][nx]["flg"] == False:
                        mi = min(mi, calc_min_allowed_D(ny,nx))
                    # 栽培中ならDの値をチェック
                    if self.grid_status[ny][nx]["flg"] == True:
                        mi = min(mi, self.grid_status[ny][nx]["D"])

            min_allowed_D[(y,x)] = mi
            return mi

        # 入り口が空きますになっていれば探索開始
        if self.grid_status[self.y_exit][0]["flg"] == False:
            calc_min_allowed_D(self.y_exit,0)
            # print(month,self.crops)
            # exit()
        
            # 植えられる作物を植える
            li = []
            for key in min_allowed_D:
                y,x = key
                li.append((dists[y][x],min_allowed_D[key],y,x))
            li.sort()
            for dist,min_allowed_d,y,x in li:
                for i in range(min(500,len(self.crops))):
                    crop_idx, s, d = self.crops[i]

                    # 今見ている作物の栽培開始時期Sが現在の月以降の場合だけ栽培可能
                    if s < month:
                        continue

                    if d - s <= MIN_SD_SPAN:
                        continue

                    # 今見ている作物の収穫時期が、そこに栽培することを許容できる最小の収穫時期を超える場合はスキップ
                    if d > min_allowed_d:
                        continue

                    # 追加栽培予定マスが道を塞ぐ場合はスキップ
                    # if not self.is_cultivatable(y,x,uf,dists, indeg_crops,d,indeg_uncrops):
                    #     continue

                    # 植える
                    self.grid_status[y][x] = {"flg":True, "idx":crop_idx, "S":s, "D":d}
                    crops_order.append((crop_idx, y, x, month))
                    if i == 0:
                        self.crops.popleft()
                    else:
                        self.crops.remove((crop_idx, s, d))
                    
                    break

        # 2ヶ月目以降の処理を実施する
        for month in range(2,self.T):
            # print(month, file=sys.stderr)
            # print(cultivatable_pos, file=sys.stderr)

            # TLE対策
            now = time.time()
            if now - self.start >= TIME_LIMIT * 0.9:
                break

            # フェーズ2：前処理
            # 栽培済マスの隣接マスを見て同じ収穫時期の野菜はUnionFindで同グループとする
            # 毎月作り直す必要あり
            uf = UnionFind(self.H*self.W)
            for y in range(self.H):
                for x in range(self.W):
                    if self.grid_status[y][x]["flg"] == False:
                        continue
                    d = self.grid_status[y][x]["D"]
                    for dy,dx in MOVE:
                        ny,nx = y+dy,x+dx
                        if self.is_movable(y,x,dy,dx) and self.grid_status[ny][nx]["flg"] == True and self.grid_status[ny][nx]["D"] == d:
                            uf.union(y*self.H + x, ny*self.H + nx)

            # 未栽培マスの一覧及び入り口から各未栽培マスへの距離をBFSで計算
            dists, cultivatable_pos = self.calc_move_dist()
            sorted_cultivatable_pos = self.cultivatable_pos_sort(cultivatable_pos, dists)
            
            # 未栽培のマスだけを通ってたどり着ける栽培済マスの入次数を計算
            indeg_crops = defaultdict(int)
            for dist, y, x in cultivatable_pos:
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if self.is_movable(y,x,dy,dx) and self.grid_status[ny][nx]["flg"] == True:
                        indeg_crops[uf.find(ny*self.W + nx)] += 1

            # 各未栽培マスへの入次数をBFSで計算
            indeg_uncrops = self.calc_indeg_uncrops(cultivatable_pos, dists)

            # フェーズ3：植える(2ヶ月目以降)
            # 栽培可能なマスのうち、入り口から遠い方から、
            # その座標に植えても通路が塞がれないマスに栽培する
            for dist, y, x in sorted_cultivatable_pos:
                # 各作物について植えられるかどうかを判定
                # TODO: 作物全てを植えるか調べるのは無駄なので適当に打ち切っている。期間等で打ち切り判定するか？
                for i in range(min(600,len(self.crops))):
                    crop_idx, s, d = self.crops[i]

                    # 今見ている作物の栽培開始時期Sが現在の月以降の場合だけ栽培可能
                    if s < month:
                        continue

                    # TODO: うまみが少ない作物は植えずにスキップさせているが、後回しにして植えるでもいいはず
                    # 乱数で植えるパターン植えないパターンを試して一番スコアいいヤツにする？
                    if month < LIMIT_END_MONTH and d - s <= MIN_SD_SPAN:
                        continue

                    # 追加栽培予定マスが道を塞ぐ場合はスキップ
                    if not self.is_cultivatable(y,x,uf,dists, indeg_crops,d,indeg_uncrops):
                        continue

                    # 植える
                    self.grid_status[y][x] = {"flg":True, "idx":crop_idx, "S":s, "D":d}
                    crops_order.append((crop_idx, y, x, month))
                    if i == 0:
                        self.crops.popleft()
                    else:
                        self.crops.remove((crop_idx, s, d))

                    # 今回植えた作物の収穫時期が隣接する作物と同じならUnionFindの同グループ化
                    for dy,dx in MOVE:
                        ny,nx = y+dy,x+dx
                        if self.is_movable(y,x,dy,dx) and self.grid_status[ny][nx]["flg"] == True:
                            if self.grid_status[ny][nx]["D"] == d:
                                uf.union(y*self.H + x, ny*self.H + nx)

                    # 今回植えた作物によって塞がれた隣接マスの入次数減と、今回植えた作物の入次数カウント
                    for dy,dx in MOVE:
                        ny,nx = y+dy,x+dx
                        if self.is_movable(y,x,dy,dx):
                            # 隣が作物ならその作物へ至る経路を1つ塞いだことになる
                            if self.grid_status[ny][nx]["flg"] == True:
                                indeg_crops[uf.find(ny*self.W + nx)] -= 1
                            else:
                                # 隣が通行可能かつより入り口に近いなら自分のマスへ至る道が1つあることになる
                                if dists[ny][nx] < dists[y][x]:
                                    indeg_crops[uf.find(y*self.W + nx)] += 1
                                # 隣が通行可能かつより入り口から遠いなら、そのマスへ至る道を1つ塞いだことになる
                                elif dists[ny][nx] > dists[y][x]:
                                    indeg_uncrops[ny][nx] -= 1

                    break
            
            # DFSの帰りがけカウントで、通路を埋めてもいい最小のDを求める
            seen = set()
            min_allowed_D = defaultdict(int)
            def calc_min_allowed_D(y,x):
                seen.add((y,x))
                mi = INF
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if self.is_movable(y,x,dy,dx):
                        # 未到達で未栽培なら探索継続
                        if (ny,nx) not in seen and self.grid_status[ny][nx]["flg"] == False:
                            mi = min(mi, calc_min_allowed_D(ny,nx))
                        # 栽培中ならDの値をチェック
                        if self.grid_status[ny][nx]["flg"] == True:
                            mi = min(mi, self.grid_status[ny][nx]["D"])

                min_allowed_D[(y,x)] = mi
                return mi

            # 入り口が空きますになっていれば探索開始
            if self.grid_status[self.y_exit][0]["flg"] == False:
                calc_min_allowed_D(self.y_exit,0)
                # print(month,self.crops)
                # exit()
            
                # 植えられる作物を植える
                li = []
                for key in min_allowed_D:
                    y,x = key
                    li.append((dists[y][x],min_allowed_D[key],y,x))
                li.sort()
                for dist,min_allowed_d,y,x in li:
                    for i in range(min(100,len(self.crops))):
                        crop_idx, s, d = self.crops[i]

                        # 今見ている作物の栽培開始時期Sが現在の月以降の場合だけ栽培可能
                        if s < month:
                            continue

                        # 今見ている作物の収穫時期が、そこに栽培することを許容できる最小の収穫時期を超える場合はスキップ
                        if d > min_allowed_d:
                            continue

                        # 追加栽培予定マスが道を塞ぐ場合はスキップ
                        # if not self.is_cultivatable(y,x,uf,dists, indeg_crops,d,indeg_uncrops):
                        #     continue

                        # 植える
                        self.grid_status[y][x] = {"flg":True, "idx":crop_idx, "S":s, "D":d}
                        crops_order.append((crop_idx, y, x, month))
                        if i == 0:
                            self.crops.popleft()
                        else:
                            self.crops.remove((crop_idx, s, d))
                        
                        break

            # フェーズ4：収穫する
            for y in range(self.H):
                for x in range(self.W):
                    if self.grid_status[y][x]["flg"] == True and self.grid_status[y][x]["D"] == month:
                        # 収穫した座標は初期化する
                        self.grid_status[y][x] = {"flg":False, "idx":-1, "S":-1, "D":-1}

            # 栽培開始時期を過ぎた作物は候補から除外
            while self.crops and self.crops[0][1] <= month:
                self.crops.popleft()

        # print(crops_order,file=sys.stderr)
        return crops_order

    # 各未栽培マスへの入次数をBFSで計算(栽培可能な場所かの判定に使用)
    def calc_indeg_uncrops(self,cultivatable_pos,dists):        
        queue = deque([[self.y_exit, 0]])
        indeg_uncrops = [[0] * self.W for _ in range(self.H)]
        indeg_uncrops[self.y_exit][0] = 1
        visited = set()
        while queue:
            y,x = queue.popleft()
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if self.is_movable(y,x,dy,dx) and (dists[ny][nx],ny,nx) in cultivatable_pos and (y,x,dy,dx) not in visited:
                    if dists[ny][nx] > dists[y][x]:
                        indeg_uncrops[ny][nx] += 1
                    queue.append([ny, nx])
                    visited.add((y,x,dy,dx))
        
        return indeg_uncrops

    # 栽培可能なマスかどうかを判定
    # 判定基準は、その座標に植えても通路が塞がれないかどうか
    def is_cultivatable(self, cand_y, cand_x, uf, dists, indeg_crops, d, indeg_uncrops):
        if [cand_y,cand_x] == [self.y_exit, 0]:
            return False

        minus = defaultdict(int)
        for dy,dx in MOVE:
            ny,nx = cand_y+dy,cand_x+dx
            # 隣接する栽培済のマスへ至る経路が無くなるようであれば栽培不可
            if self.is_movable(cand_y,cand_x,dy,dx):
                # 隣が栽培済
                if self.grid_status[ny][nx]["flg"] == True:
                    # 収穫時期が異なっていて経路を塞ぐ場合は入次数を減らす
                    if self.grid_status[ny][nx]["D"] != d:
                        minus[uf.find(ny*self.W + nx)] += 1
                # 隣が未栽培かつ入り口からより遠くて、そのマスへ至る道を完全に塞いでしまう場合
                elif dists[ny][nx] > dists[cand_y][cand_x] and indeg_uncrops[ny][nx] - 1 <= 0:
                    return False

        # 収穫時期が異なっていて経路を完全に塞ぐ(入次数が0)場合は栽培不可(収穫時期が同じなら到達可能)
        for key in minus:
            if indeg_crops[key] - minus[key] <= 0:
                return False

        return True
    
    # 栽培可能なマスを距離が遠くて隣接するマスから順に見られるようにソート
    def cultivatable_pos_sort(self, cultivatable_pos, dists):

        sorted_cultivatable_pos = []

        hq = []
        for dist,y,x in cultivatable_pos:
            heappush(hq, (-dist,y,x))

        seen = set()
        while hq:
            dist,y,x = heappop(hq)
            dist = -dist

            if (dist,y,x) in seen:
                continue

            # 未チェックで一番距離が遠いマスを追加
            sorted_cultivatable_pos.append((dist,y,x))
            seen.add((dist,y,x))

            # そのマスに隣接する栽培可能マスもBFSで探索してついでに追加
            queue = deque([[y,x]])
            visited = [[-1]*self.W for _ in range(self.H)]
            visited[y][x] = 0
            while queue:
                y,x = queue.popleft()
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if self.is_movable(y,x,dy,dx) and (dists[ny][nx], ny, nx) in cultivatable_pos and (dists[ny][nx], ny, nx) not in seen and visited[ny][nx] == -1:
                        visited[ny][nx] = visited[y][x] + 1
                        if visited[ny][nx] <= 1:
                            queue.append([ny, nx])

                        sorted_cultivatable_pos.append((dists[ny][nx], ny, nx))
                        seen.add((dists[ny][nx], ny, nx))

        return sorted_cultivatable_pos
    
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
