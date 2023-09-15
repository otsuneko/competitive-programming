import sys
import time
import random
from collections import deque
from collections import defaultdict
from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport
sys.setrecursionlimit(10**7)

# 定数
TIME_LIMIT = 10.0
INF = 10**18
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1]) #縦横

# フェーズ2-1：栽培可能なマスのうち入り口から遠いものから、植えても通路が塞がれないマスに栽培する
MAX_SEARCH_CROPS = 1000 # Dが小さい方から最大何個の作物を栽培候補として探索するかの閾値
POS_SORT_BFS_DIST = 0 # 栽培マスを入り口から遠い順にソートする際に隣接マスをBFSで探索する時の距離
MIN_SD_SPAN = 8 # D-Sがこの値以下の作物はうまみが少ないとしてスキップ
LIMIT_END_MONTH = 90 # MIN_SD_SPANを無くす月

# フェーズ2-2：未栽培マスでできた通路に対し、DFSの帰りがけカウントでそのマスで栽培可能な最大のDを求め、植える
DFS_BACK_DIST = 5 # 遠くのマスから入り口に向けて戻ってくる際に、何マス分戻って栽培するかの閾値
ALLOWED_D_DIFF = 0 # 通路上のマスに置ける最大のDからどれだけ引いた値まで許容するか

# フェーズ2-3：入口付近で収穫時期が近い作物を栽培する(特に最序盤(T<=10)の無駄を省く目的)
ENTRY_BFS_DIST = 5 # 入り口付近をBFSで栽培する時の探索距離
MAX_FUTURE_MONTH = 10 # 栽培可能な作物の収穫時期が現在の月から数えてこの値以上先なら栽培しない


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
        # print(*self.crops[:100], sep="\n", file=sys.stderr)
        self.crops = deque(self.crops)

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
    
    # 初月だけの栽培計画の立て方
    def ini_cultivate_plan(self,month,crops_order):

        longest_path = self.calc_longest_path(y,x)

        # 道の脇に植えていく戦略
        self.harvest_month = 30
        crops = deque()
        num_per_D = defaultdict(int)
        for crop_idx,s,d in self.crops:
            if d > self.harvest_month:
                break
            crops.append((crop_idx,s,d))
            if d - s <= MIN_SD_SPAN:
                num_per_D[d] += 1
        crops.reverse()

        for dist,(y,x) in enumerate(longest_path):
            for dy,dx in MOVE:
                cy,cx = y,x
                ny,nx = cy+dy,cx+dx
                fixed_d = -1
                # 道の脇に植える
                while 1:
                    # print(cy,cx,ny,nx)
                    if self.is_movable(cy,cx,dy,dx) and self.grid_status[ny][nx]["flg"] == False and [ny,nx] not in longest_path:
                        for i in range(min(MAX_SEARCH_CROPS,len(crops))):
                            crop_idx, s, d = crops[i]

                            # 今見ている作物の栽培開始時期Sが現在の月以降の場合だけ栽培可能
                            if s < month:
                                continue

                            if fixed_d != -1 and d != fixed_d:
                                continue

                            if d > 8 - dist:
                                continue

                            # 植える
                            self.grid_status[ny][nx] = {"flg":True, "idx":crop_idx, "S":s, "D":d}
                            crops_order.append((crop_idx, ny, nx, month))
                            fixed_d = d
                            self.crops.remove((crop_idx, s, d))
                            if i == 0:
                                crops.popleft()
                            else:
                                crops.remove((crop_idx, s, d))

                            # 更に突き進む
                            cy,cx = ny,nx
                            ny,nx = ny+dy,nx+dx

                            break
                        else:
                            break
                    else:
                        break

            self.harvest_month -= 1


    # 作物の栽培&収穫計画を作成
    def create_cultivate_plan(self):
        crops_order = [] # 栽培する作物のID、座標、何ヶ月目に植えるかの情報

        # 毎月の処理を実施する
        for month in range(1,self.T):
            # print(month, file=sys.stderr)

            # TLE対策
            now = time.time()
            if now - self.start >= TIME_LIMIT * 0.9:
                break      

            # フェーズ1：前処理
            # 未栽培マスの一覧及び入り口から各未栽培マスへの距離をBFSで計算
            # print("Phase.1",file=sys.stderr)
            dists, cultivatable_pos = self.calc_move_dist()
            sorted_cultivatable_pos = self.cultivatable_pos_sort(cultivatable_pos, dists)

            # 栽培済マスの隣接マスを見て同じ収穫時期の野菜はUnionFindで同グループとする
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
            
            # 未栽培のマスだけを通ってたどり着ける栽培済マスの入次数を計算
            indeg_crops = defaultdict(int)
            for dist, y, x in cultivatable_pos:
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if self.is_movable(y,x,dy,dx) and self.grid_status[ny][nx]["flg"] == True:
                        # 迂回して辿り着くルートも考慮に入れるため、距離の比較はしない
                        indeg_crops[uf.find(ny*self.W + nx)] += 1

            # 各未栽培マスへの入次数をBFSで計算
            indeg_uncrops = self.calc_indeg_uncrops(cultivatable_pos, dists)

            # フェーズ2：植える
            # フェーズ2-1：栽培可能なマスのうち入り口から遠いものから、植えても通路が塞がれないマスに栽培する
            # print("Phase.2-1",file=sys.stderr)
            if month == 1:
                self.ini_cultivate_plan(month,crops_order)
            else:
                for dist, y, x in sorted_cultivatable_pos:
                    for i in range(min(MAX_SEARCH_CROPS,len(self.crops))):
                        crop_idx, s, d = self.crops[i]

                        # 今見ている作物の栽培開始時期Sが現在の月と等しい場合だけ栽培可能
                        if s != month:
                            continue
                        # if s < month or d > month + 20:
                        #     continue

                        # 得点が少ない(D-Sが小さい)作物は植えずにスキップ
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
                
            # フェーズ2-2：未栽培マスでできた通路に対し、DFSの帰りがけカウントでそのマスで栽培可能な最大のDを求め、植える
            def calc_max_allowed_D(y,x,seen,max_allowed_D,depth):
                seen.add((y,x))
                max_D = INF
                max_depth = depth

                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if self.is_movable(y,x,dy,dx):
                        # 未到達で未栽培なら探索継続
                        if (ny,nx) not in seen and self.grid_status[ny][nx]["flg"] == False:
                            tmp_D,tmp_depth = calc_max_allowed_D(ny,nx,seen,max_allowed_D,depth+1)
                            max_D = min(max_D, tmp_D)
                            max_depth = max(max_depth,tmp_depth)
                        # 栽培中ならDの値をチェック
                        if self.grid_status[ny][nx]["flg"] == True:
                            max_D = min(max_D, self.grid_status[ny][nx]["D"])

                if self.grid_status[y][x]["flg"] == False:
                    # 最初の10ヶ月程度は入口付近でD<10の作物を栽培するため、そのスペース確保用に制限を設ける
                    # if month < 10 and depth <= max_depth - DFS_BACK_DIST:
                    #     pass
                    # else:
                        for diff in range(ALLOWED_D_DIFF+1):
                            for i in range(min(MAX_SEARCH_CROPS,len(self.crops))):
                                crop_idx, s, d = self.crops[i]

                                # 今見ている作物の栽培開始時期Sが現在の月以降の場合だけ栽培可能
                                if s < month:
                                    continue

                                # 今見ている作物の収穫時期が、そこに栽培することを許容できる最大の収穫時期でない場合はスキップ
                                if d != max_D-diff:
                                    continue

                                # 植える
                                self.grid_status[y][x] = {"flg":True, "idx":crop_idx, "S":s, "D":d}
                                crops_order.append((crop_idx, y, x, month))
                                max_D = min(max_D, max_D-diff)
                                if i == 0:
                                    self.crops.popleft()
                                else:
                                    self.crops.remove((crop_idx, s, d))
                                
                                break
                            else:
                                continue
                            break

                max_allowed_D[(y,x)] = max_D
                return max_allowed_D[(y,x)], max_depth

            # 入り口が空きマスになっていれば探索開始
            if self.grid_status[self.y_exit][0]["flg"] == False:
                seen = set()
                max_allowed_D = defaultdict(int)
                # print(month, "before:",len(crops_order))
                # print("Phase.2-2",file=sys.stderr)
                # calc_max_allowed_D(self.y_exit,0,seen,max_allowed_D,0)
                # print(month,"after:",len(crops_order))

                # フェーズ2-3：入口付近で収穫時期が近い作物を栽培する(特に最序盤(T<=10)の無駄を省く目的)
                # print("Phase.2-3",file=sys.stderr)
                longest_path = self.calc_longest_path()
                # BFS戦略
                # queue = deque([[self.y_exit, 0]])
                # visited = [[-1]*self.W for _ in range(self.H)]
                # visited[self.y_exit][0] = 0
                # while queue:
                #     y,x = queue.popleft()
                #     for i in range(len(self.crops)):
                #         crop_idx, s, d = self.crops[i]
                        
                #         # 今見ている作物の栽培開始時期Sが現在の月より前の場合は栽培不可
                #         if s < month:
                #             continue

                #         # そのマスで栽培可能な最大のDを超えるか、month+MAX_FUTURE_MONTHを超える場合はスキップ
                #         if d > min(month+MAX_FUTURE_MONTH, max_allowed_D[(y,x)]):
                #             continue

                #         # 奥へ続く通路を塞ぐのはだめ
                #         if (y,x) in longest_path:
                #             continue

                #         self.grid_status[y][x] = {"flg":True, "idx":crop_idx, "S":s, "D":d}
                #         crops_order.append((crop_idx, y, x, month))
                #         if i == 0:
                #             self.crops.popleft()
                #         else:
                #             self.crops.remove((crop_idx, s, d))

                #         break

                #     # 次の栽培可能マスを探索
                #     for dy,dx in MOVE:
                #         ny,nx = y+dy,x+dx
                #         if self.is_movable(y,x,dy,dx) and self.grid_status[ny][nx]["flg"] == False and visited[ny][nx] == -1:
                #             visited[ny][nx] = visited[y][x] + 1
                #             if visited[ny][nx] <= ENTRY_BFS_DIST:
                #                 queue.append([ny, nx])

            # フェーズ3：収穫する
            # print("Phase.3",file=sys.stderr)
            for y in range(self.H):
                for x in range(self.W):
                    if self.grid_status[y][x]["flg"] == True and self.grid_status[y][x]["D"] == month:
                        # 収穫した座標は初期化する
                        self.grid_status[y][x] = {"flg":False, "idx":-1, "S":-1, "D":-1}

            # 栽培開始時期を過ぎた作物は候補から除外
            while self.crops and self.crops[0][1] <= month:
                # print(self.crops[0])
                self.crops.popleft()

        # print(crops_order,file=sys.stderr)
        return crops_order

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
                        if visited[ny][nx] <= POS_SORT_BFS_DIST:
                            queue.append([ny, nx])
                            sorted_cultivatable_pos.append((dists[ny][nx], ny, nx))
                        seen.add((dists[ny][nx], ny, nx))

        return sorted_cultivatable_pos
    
    # BFSで最長経路を算出
    def calc_longest_path(self):
        # 入り口が埋まってたら経路長0
        if self.grid_status[self.y_exit][0]["flg"] == True:
            return []

        queue = deque([[self.y_exit, 0]])
        prev = [[[-1,-1] for _ in range(self.W)] for _ in range(self.H)]
        prev[self.y_exit][0] = [-INF,-INF]
        visited = [[-1] * self.W for _ in range(self.H)]
        visited[self.y_exit][0] = 0
        longest_pos = [-1,-1]
        max_dist = -1
        while queue:
            y,x = queue.popleft()
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if self.is_movable(y,x,dy,dx) and self.grid_status[ny][nx]["flg"] == False and prev[ny][nx] == [-1,-1]:
                    prev[ny][nx] = [y,x]
                    visited[ny][nx] = visited[y][x] + 1
                    if visited[ny][nx] > max_dist:
                        max_dist = visited[ny][nx]
                        longest_pos = [ny,nx]
                    queue.append([ny, nx])
        
        cur = longest_pos
        longest_path = [cur]
        while cur != [-INF,-INF]:
            y,x = cur
            cur = prev[y][x]
            longest_path.append(cur)

        longest_path = longest_path[:-1][::-1]

        return longest_path

# BFSで指定した座標までの最短経路を算出(ゴールから入り口へのパス順)
    def calc_reversed_path(self,gy,gx):

        queue = deque([[self.y_exit, 0]])
        prev = [[[-1,-1] for _ in range(self.W)] for _ in range(self.H)]
        prev[self.y_exit][0] = [-INF,-INF]
        while queue:
            y,x = queue.popleft()
            if [y,x] == [gy,gx]:
                break
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if self.is_movable(y,x,dy,dx) and prev[ny][nx] == [-1,-1]:
                    prev[ny][nx] = [y,x]
                    queue.append([ny, nx])

        cur = (gy,gx)
        path = [cur]
        while cur != (-INF,-INF):
            y,x = cur
            cur = tuple(prev[y][x])
            path.append(cur)

        return path[:-1]

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
