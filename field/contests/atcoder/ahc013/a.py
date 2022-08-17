import random
import sys
import time
from copy import deepcopy
from collections import defaultdict

# 結果格納用
class Result:

    def __init__(self, moves, connects):
        self.moves = moves
        self.connects = connects

# 回答用
class Solver:
    MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])

    def __init__(self, N, K, field, start, param):
        self.N = N
        self.K = K
        self.field = field
        self.start = start
        self.param = param
        self.computers = defaultdict()
        cp_id = 0
        for y in range(N):
            for x in range(N):
                if field[y][x][0] != 0:
                    self.computers[(y,x)] = [cp_id, field[y][x][0]]
                    cp_id += 1
        self.uf = UnionFind(K*100)
        self.LIM = K*100

    # PCを動かせるマスのうち一番有利な方向へ1マス動かす
    def _move(self, lim, moves, connects):

        # 移動後のマスの上下左右に存在する同じ種類のPCの数とその近さを基にスコア化
        def calc_goodness(y,x,ori_y,ori_x,kind,isConnected):
            goodness = 0
            # 移動することで上下方向(y方向)に空きスペースができる場合は上下を探索
            if y - ori_y == 0:
                DIR = [[1,0],[-1,0]]
            # 移動することで左右方向(x方向)に空きスペースができる場合は左右を探索
            else:
                DIR = [[0,1],[0,-1]]
            
            # 探索開始地点が同種PCのケーブル上の場合
            if self.field[y][x][0] == kind+5:
                pcid = self.uf.find(self.computers[(ori_y,ori_x)][0])
                pcid2 = self.uf.find(self.computers[tuple(self.field[y][x][2])][0])
                # 同種PCのケーブルに割り込み接続する場合
                if pcid != pcid2:
                    # 接続元のクラスタの大きさ
                    ori_size = self.uf.size(self.computers[(ori_y,ori_x)][0])
                    # 接続先のクラスタの大きさ
                    to_size = self.uf.size(self.computers[tuple(self.field[y][x][2])][0])
                    # 接続後のnC2が嬉しさとなる
                    goodness = (ori_size+to_size)*(ori_size+to_size-1)//2
                # ケーブルを縮める場合(同じクラスタのケーブル上にいる場合)
                else:
                    # 縮めた後のPC自体が接続できるPCがあるか
                    pc_cnt = 1
                    dist_sum = 1
                    seen = set([self.uf.find(self.computers[(ori_y,ori_x)][0])]) # クラスタの重複カウント防止用
                    for mv in DIR:
                        ny,nx = y+mv[0], x+mv[1]
                        dist = 1
                        while 0 <= ny < self.N and 0 <= nx < self.N:
                            if self.field[ny][nx][0] == 0:
                                ny,nx = ny+mv[0], nx+mv[1]
                                dist += 1
                                continue
                            else:
                                if self.field[ny][nx][0] == kind and self.uf.find(self.computers[(ny,nx)][0]) not in seen:
                                    seen.add(self.uf.find(self.computers[(ny,nx)][0]))
                                    cluster_size = self.uf.size(self.computers[(ny,nx)][0])
                                    pc_cnt += cluster_size
                                    dist_sum += dist
                                break
                    # 縮めて生まれたスペースによって接続できるようになったPCがあるか
                    tmp_pc_cnt = 0
                    tmp_dist_sum = 0
                    pc_pair = []
                    for mv in DIR:
                        ny,nx = ori_y+mv[0], ori_x+mv[1]
                        dist = 1
                        while 0 <= ny < self.N and 0 <= nx < self.N:
                            if self.field[ny][nx][0] == 0:
                                ny,nx = ny+mv[0], nx+mv[1]
                                dist += 1
                                continue
                            else:
                                if 1 <= self.field[ny][nx][0] <= 5:
                                    pc_pair.append((self.uf.find(self.computers[(ny,nx)][0]), self.computers[(ny,nx)][1]))
                                    cluster_size = self.uf.size(self.computers[(ny,nx)][0])
                                    tmp_pc_cnt += cluster_size
                                    tmp_dist_sum += dist
                                break
                    # ぶつかったPCが2台で、別のクラスタに所属し、同じ種類の場合のみ嬉しさを計算
                    if len(pc_pair) == 2 and pc_pair[0][0] != pc_pair[1][0] and pc_pair[0][1] == pc_pair[1][1]:
                        pc_cnt += tmp_pc_cnt
                        dist_sum += tmp_dist_sum
                    goodness = pc_cnt*(pc_cnt-1)//2 / (dist_sum**0.25)

            # 探索開始地点が空きマスの場合
            elif self.field[y][x][0] == 0:
                # 移動した後のPC自体が接続できるPCがあるか
                pc_cnt = 1
                dist_sum = 1
                seen = set([self.uf.find(self.computers[(ori_y,ori_x)][0])]) # クラスタの重複カウント防止用
                for mv in DIR:
                    ny,nx = y+mv[0], x+mv[1]
                    dist = 1
                    while 0 <= ny < self.N and 0 <= nx < self.N:
                        if self.field[ny][nx][0] == 0:
                            ny,nx = ny+mv[0], nx+mv[1]
                            dist += 1
                            continue
                        else:
                            if self.field[ny][nx][0] == kind and self.uf.find(self.computers[(ny,nx)][0]) not in seen:
                                seen.add(self.uf.find(self.computers[(ny,nx)][0]))
                                cluster_size = self.uf.size(self.computers[(ny,nx)][0])
                                pc_cnt += cluster_size
                                dist_sum += dist
                            break
                # 移動して生まれたスペースによって接続できるようになったPCがあるか(ケーブル未接続の場合のみ考慮)
                if not isConnected:
                    tmp_pc_cnt = 0
                    tmp_dist_sum = 0
                    pc_pair = []
                    seen = set([self.uf.find(self.computers[(ori_y,ori_x)][0])]) # クラスタの重複カウント防止用
                    for mv in DIR:
                        ny,nx = ori_y+mv[0], ori_x+mv[1]
                        dist = 1
                        while 0 <= ny < self.N and 0 <= nx < self.N:
                            if self.field[ny][nx][0] == 0:
                                ny,nx = ny+mv[0], nx+mv[1]
                                dist += 1
                                continue
                            else:
                                if 1 <= self.field[ny][nx][0] <= 5:
                                    pc_pair.append((self.uf.find(self.computers[(ny,nx)][0]), self.computers[(ny,nx)][1]))
                                    cluster_size = self.uf.size(self.computers[(ny,nx)][0])
                                    tmp_pc_cnt += cluster_size
                                    tmp_dist_sum += dist
                                break
                    # ぶつかったPCが2台で、別のクラスタに所属し、同じ種類の場合のみ嬉しさを計算
                    if len(pc_pair) == 2 and pc_pair[0][0] != pc_pair[1][0] and pc_pair[0][1] == pc_pair[1][1]:
                        pc_cnt += tmp_pc_cnt
                        dist_sum += tmp_dist_sum
                # 接続後のnC2を距離で重み付けしたものが嬉しさとなる
                goodness = pc_cnt*(pc_cnt-1)//2 / (dist_sum**0.25)
            
            return goodness
        
        # PCを動かせるマスのうち一番有利な方向へ1マス動かす
        max_goodness = 0
        max_pcid = max_kind = -1
        max_ny,max_nx = None,None
        max_y,max_x = None,None
        for y,x in list(self.computers.keys()):
            goodness = 0
            pcid = self.computers[(y,x)][0]
            kind = self.computers[(y,x)][1]
            # ケーブルに接続されている場合
            if self.field[y][x][1] == True:
                connect_cnt = 0
                for mv in self.MOVE:
                    ny,nx = y+mv[0],x+mv[1]
                    if not (0<=ny<self.N and 0<=nx<self.N):
                        continue
                    if self.field[ny][nx][0] in [kind,kind+5]:
                        # print(max_y,max_x,max_ny,max_nx,max_kind,self.field[max_y][max_x], self.field[max_ny][max_nx])
                        if self.field[ny][nx][0] == kind:
                            pcid2 = self.computers[(ny,nx)][0]
                        elif self.field[ny][nx][0] == kind+5:
                            pcid2 = self.computers[tuple(self.field[ny][nx][3])][0]
                        if self.uf.find(pcid) == self.uf.find(pcid2):
                            connect_cnt += 1

                # 複数接続済みのPCはスキップ
                if connect_cnt > 1:
                    continue
                ny,nx = None,None
                ny2,nx2 = None,None
                for mv in self.MOVE:
                    ny,nx = y+mv[0],x+mv[1]
                    if not (0<=ny<self.N and 0<=nx<self.N):
                        continue
                    if self.field[ny][nx][0] in [kind,kind + 5]:
                        if self.field[ny][nx][0] == kind:
                            pcid2 = self.computers[(ny,nx)][0]
                        elif self.field[ny][nx][0] == kind+5:
                            pcid2 = self.computers[tuple(self.field[ny][nx][3])][0]
                        if self.uf.find(pcid) == self.uf.find(pcid2):
                            # ケーブルが接続されているのと逆方向に進む
                            ny,nx = y-mv[0],x-mv[1]
                            # ケーブルが接続されている側に縮める
                            ny2,nx2 = y+mv[0],x+mv[1]
                            break
                else:
                    continue
                # ケーブルを延長する場合
                if 0<=ny<self.N and 0<=nx<self.N and self.field[ny][nx][0] in [0,kind+5]:
                    goodness = calc_goodness(ny,nx,y,x,kind,self.field[y][x][1])
                    if goodness > max_goodness:
                        max_goodness = goodness
                        max_pcid = pcid
                        max_kind = kind
                        max_ny,max_nx = ny,nx
                        max_y,max_x = y,x

                # ケーブルを縮める場合
                if 0<=ny2<self.N and 0<=nx2<self.N and self.field[ny2][nx2][0] == kind+5:
                    goodness = calc_goodness(ny2,nx2,y,x,kind,self.field[y][x][1])
                    if goodness > max_goodness:
                        max_goodness = goodness
                        max_pcid = pcid
                        max_kind = kind
                        max_ny,max_nx = ny2,nx2
                        max_y,max_x = y,x

            # ケーブルに接続されてない場合
            else:
                for mv in self.MOVE:
                    ny,nx = y+mv[0],x+mv[1]
                    if not (0<=ny<self.N and 0<=nx<self.N):
                        continue
                    # 隣接するマスが空きマスか、自分と同種のPCを接続するケーブルマス以外はスキップ
                    if self.field[ny][nx][0] not in [0,kind+5]:
                        continue
                    # 空きマスが見つかった場合は移動後の嬉しさを計算
                    goodness = calc_goodness(ny,nx,y,x,kind,self.field[y][x][1])

                    if goodness > max_goodness:
                        max_goodness = goodness
                        max_pcid = pcid
                        max_kind = kind
                        max_ny,max_nx = ny,nx
                        max_y,max_x = y,x
        
        # 移動しても嬉しさが増えなければ終了
        if max_goodness == 0:
            return

        # ケーブル延長or縮小の場合(既にケーブル接続済みの場合)
        if self.field[max_y][max_x][1] == True:
            # 延長する場合(=移動先が空マスか別クラスタの場合)
            if self.field[max_ny][max_nx][0] == 0 or (self.field[max_ny][max_nx][0] == max_kind+5 and self.uf.find(max_pcid) != self.uf.find(self.computers[tuple(self.field[max_ny][max_nx][2])][0])):
                # ケーブル割り込み接続の場合(移動先が別クラスタの場合)
                if self.field[max_ny][max_nx][0] == max_kind+5 and self.uf.find(max_pcid) != self.uf.find(self.computers[tuple(self.field[max_ny][max_nx][2])][0]):
                    # 未接続のPCを、接続済みのケーブルに割り込ませる
                    p1 = self.field[max_ny][max_nx][2]
                    p2 = self.field[max_ny][max_nx][3]
                    # 現在接続されているケーブルを切断
                    connects.remove(tuple([*p1,*p2]))
                    # 繋ぎ直し
                    connects.add(tuple([*p1,max_ny,max_nx]))
                    connects.add(tuple([max_ny,max_nx,*p2]))

                    # fieldの更新
                    # self.field[max_ny][max_nx] = [max_kind,True,p1[:],p2[:]]

                    # UF上のPCのクラスタリング
                    self.uf.unite(self.computers[(max_y,max_x)][0],self.computers[tuple(p1)][0])

                    # 水平(x方向)に繋ぐ場合
                    if max_ny == p1[0] == p2[0]:
                        # 接続元の情報を更新
                        nx = max_nx-1
                        while nx >= p1[1]:
                            self.field[max_ny][nx][3] = [max_ny,max_nx]
                            nx -= 1
                        # 接続先の情報を更新
                        nx = max_nx+1
                        while nx <= p2[1]:
                            self.field[max_ny][nx][2] = [max_ny,max_nx]
                            nx += 1
                    # 垂直(y方向)に繋ぐ場合
                    elif max_nx == p1[1] == p2[1]:
                        # 接続元の情報を更新
                        ny = max_ny-1
                        while ny >= p1[0]:
                            self.field[ny][max_nx][3] = [max_ny,max_nx]
                            ny -= 1
                        # 接続先の情報を更新
                        ny = max_ny+1
                        while ny <= p2[0]:
                            self.field[ny][max_nx][2] = [max_ny,max_nx]
                            ny += 1
                    else:
                        AssertionError()

                # 移動先が空マスでも別クラスタでも実行する処理(伸ばしてきたのと同じ軸の繋ぎ直し)
                # 右か下に移動する場合
                if max(max_ny-max_y,max_nx-max_x) > 0:
                    from_pc = self.field[max_y][max_x][2]
                    # 現在接続されているケーブルを切断
                    connects.remove(tuple([*from_pc,max_y,max_x]))
                    # 延長先で繋ぎ直し
                    connects.add(tuple([*from_pc,max_ny,max_nx]))
                    self.field[max_y][max_x] = [max_kind+5,True,from_pc,[max_ny,max_nx]]
                    self.field[max_ny][max_nx] = [max_kind,True,from_pc,[max_ny,max_nx]]
                    # 右に移動する場合
                    if max_ny == from_pc[0]:
                        # 接続元の情報を更新
                        nx = max_nx-1
                        while nx >= from_pc[1]:
                            self.field[max_ny][nx][3] = [max_ny,max_nx]
                            nx -= 1
                    # 下に移動する場合
                    elif max_nx == from_pc[1]:
                        # 接続元の情報を更新
                        ny = max_ny-1
                        while ny >= from_pc[0]:
                            self.field[ny][max_nx][3] = [max_ny,max_nx]
                            ny -= 1
                # 左か上に移動する場合
                else:
                    to_pc = self.field[max_y][max_x][3]
                    # 現在接続されているケーブルを切断
                    connects.remove(tuple([max_y,max_x,*to_pc]))
                    # 延長先で繋ぎ直し
                    connects.add(tuple([max_ny,max_nx,*to_pc]))
                    self.field[max_y][max_x] = [max_kind+5,True,[max_ny,max_nx],to_pc]
                    self.field[max_ny][max_nx] = [max_kind,True,[max_ny,max_nx],to_pc]
                    # 左に移動する場合
                    if max_ny == to_pc[0]:
                        # 接続先の情報を更新
                        nx = max_nx+1
                        while nx <= to_pc[1]:
                            self.field[max_ny][nx][2] = [max_ny,max_nx]
                            nx += 1
                    # 上に移動する場合
                    elif max_nx == to_pc[1]:
                        # 接続先の情報を更新
                        ny = max_ny+1
                        while ny <= to_pc[0]:
                            self.field[ny][max_nx][2] = [max_ny,max_nx]
                            ny += 1

            # 縮小する場合(=移動先が同じクラスタの場合)
            else:
                # 短縮ではなく、延長して自分と同じクラスタにぶつかった場合は終了
                if self.field[max_ny][max_nx][2] != self.field[max_y][max_x][2]:
                    return
                # 右か下に移動する場合
                if max(max_ny-max_y,max_nx-max_x) > 0:
                    to_pc = self.field[max_y][max_x][3]
                    # 現在接続されているケーブルを切断
                    connects.remove(tuple([max_y,max_x,*to_pc]))
                    # 縮小先で繋ぎ直し
                    connects.add(tuple([max_ny,max_nx,*to_pc]))
                    self.field[max_y][max_x] = [0,False,[-1,-1],[-1,-1]]
                    self.field[max_ny][max_nx] = [max_kind,True,[max_ny,max_nx],to_pc]
                    # 右に移動する場合
                    if max_ny == to_pc[0]:
                        # 接続元の情報を更新
                        nx = max_nx+1
                        while nx <= to_pc[1]:
                            self.field[max_ny][nx][2] = [max_ny,max_nx]
                            nx += 1
                    # 下に移動する場合
                    elif max_nx == to_pc[1]:
                        # 接続元の情報を更新
                        ny = max_ny+1
                        while ny <= to_pc[0]:
                            self.field[ny][max_nx][2] = [max_ny,max_nx]
                            ny += 1
                # 左か上に移動する場合
                else:
                    from_pc = self.field[max_y][max_x][2]
                    # 現在接続されているケーブルを切断
                    connects.remove(tuple([*from_pc,max_y,max_x]))
                    # 縮小先で繋ぎ直し
                    connects.add(tuple([*from_pc,max_ny,max_nx]))
                    self.field[max_y][max_x] = [0,False,[-1,-1],[-1,-1]]
                    self.field[max_ny][max_nx] = [max_kind,True,from_pc,[max_ny,max_nx]]
                    # 左に移動する場合
                    if max_ny == from_pc[0]:
                        # 接続先の情報を更新
                        nx = max_nx-1
                        while nx >= from_pc[1]:
                            self.field[max_ny][nx][3] = [max_ny,max_nx]
                            nx -= 1
                    # 上に移動する場合
                    elif max_nx == from_pc[1]:
                        # 接続先の情報を更新
                        ny = max_ny-1
                        while ny >= from_pc[0]:
                            self.field[ny][max_nx][3] = [max_ny,max_nx]
                            ny -= 1
        # ケーブル未接続の場合
        else:
            # 移動先が同じ種類のPCケーブルの場合
            if self.field[max_ny][max_nx][0] == max_kind+5:
                max_pcid2 = self.computers[tuple(self.field[max_ny][max_nx][2])][0]
                # ケーブル割り込み接続の場合(移動先が別クラスタの場合)
                if self.uf.find(max_pcid) != self.uf.find(max_pcid2):
                    
                    # 未接続のPCを、接続済みのケーブルに割り込ませる
                    p1 = self.field[max_ny][max_nx][2]
                    p2 = self.field[max_ny][max_nx][3]
                    # 現在接続されているケーブルを切断
                    connects.remove(tuple([*p1,*p2]))
                    # 繋ぎ直し
                    connects.add(tuple([*p1,max_ny,max_nx]))
                    connects.add(tuple([max_ny,max_nx,*p2]))

                    # fieldの更新
                    self.field[max_ny][max_nx] = [max_kind,True,p1[:],p2[:]]
                    self.field[max_y][max_x] = [0,False,[-1,-1],[-1,-1]]

                    # UF上のPCのクラスタリング
                    self.uf.unite(self.computers[(max_y,max_x)][0],self.computers[tuple(p1)][0])

                    # 水平(x方向)に繋ぐ場合
                    if max_ny == p1[0] == p2[0]:
                        # 接続元の情報を更新
                        nx = max_nx-1
                        while nx >= p1[1]:
                            self.field[max_ny][nx][3] = [max_ny,max_nx]
                            nx -= 1
                        # 接続先の情報を更新
                        nx = max_nx+1
                        while nx <= p2[1]:
                            self.field[max_ny][nx][2] = [max_ny,max_nx]
                            nx += 1
                    # 垂直(y方向)に繋ぐ場合
                    elif max_nx == p1[1] == p2[1]:
                        # 接続元の情報を更新
                        ny = max_ny-1
                        while ny >= p1[0]:
                            self.field[ny][max_nx][3] = [max_ny,max_nx]
                            ny -= 1
                        # 接続先の情報を更新
                        ny = max_ny+1
                        while ny <= p2[0]:
                            self.field[ny][max_nx][2] = [max_ny,max_nx]
                            ny += 1
                    else:
                        AssertionError()
            else:
                self.field[max_ny][max_nx] = [max_kind,False,[-1,-1],[-1,-1]]
                self.field[max_y][max_x] = [0,False,[-1,-1],[-1,-1]]
        
        # self.field[max_ny][max_nx][0] = max_kind
        self.computers[(max_ny,max_nx)] = [max_pcid, max_kind]
        self.computers.pop((max_y,max_x))
        moves.append((max_y,max_x,max_ny,max_nx))

    # 同じ列or行にあって、間に邪魔者がいない未接続のコンピュータ同士を接続する
    def _connect(self, lim: int, connects):

        # 接続した時の嬉しさをスコア化
        def calc_goodness(y,x,mv):
            p1 = self.computers[(y,x)]
            goodness = 0
            pc_cnt = self.uf.size(p1[0])
            dist = 1
            ny,nx = y+mv[0], x+mv[1]
            while ny < self.N and nx < self.N:
                if self.field[ny][nx][0] == self.field[y][x][0]:
                    p2 = self.computers[(ny,nx)]
                    pc_cnt += self.uf.size(p2[0])
                    goodness = pc_cnt*(pc_cnt-1)//2 / (dist**1.5)
                ny += mv[0]
                nx += mv[1]
                dist += 1
            return goodness

        def can_connect(y, x, mv):
            ny,nx = y+mv[0], x+mv[1]
            while ny < self.N and nx < self.N:
                if self.field[ny][nx][0] == 0:
                    ny,nx = ny+mv[0], nx+mv[1]
                    continue
                # PCの種別が同じで、かつその接続が未実施の場合
                elif self.field[ny][nx][0] == self.field[y][x][0] and (y,x,ny,nx) not in connects:
                    # 同じクラスタに既に属している場合は接続不要
                    if self.uf.find(self.computers[(y,x)][0]) != self.uf.find(self.computers[(ny,nx)][0]):
                        return True,(ny,nx)
                    else:
                        return False, None
                else:
                    return False, None
            return False, None

        # 接続をシミュレーション
        # グリッドの種類…0：何もない、1~5：PCがある、6~10：PC番号+5のケーブルが存在
        # true：接続中、false：未接続
        # 接続元PCの座標(boolがtrueの場合のみ使用)
        # 接続先PCの座標(boolがtrueの場合のみ使用)
        def do_connect(y,x,mv,to):
            # 接続元PCの状態を更新
            self.field[y][x][1] = True
            self.field[y][x][2] = [y,x][:]
            self.field[y][x][3] = to[:]

            # ケーブル、接続先PCの状態を更新
            ny,nx = y+mv[0], x+mv[1]
            while ny < self.N and nx < self.N:
                # まだ接続先のPCにたどり着いていない時
                if self.field[ny][nx][0] == 0:
                    self.field[ny][nx][0] = self.field[y][x][0] + 5
                    self.field[ny][nx][1] = True
                    self.field[ny][nx][2] = [y,x][:]
                    self.field[ny][nx][3] = to[:]
                # 接続先のPCにたどり着いた時
                elif self.field[ny][nx][0] == self.field[y][x][0]:
                    self.field[ny][nx][1] = True
                    self.field[ny][nx][2] = [y,x][:]
                    self.field[ny][nx][3] = to[:]
                    connects.add((y,x,*to))
                    # UFはPCのIDで結合
                    self.uf.unite(self.computers[(y,x)][0],self.computers[to][0])
                    return
                else:
                    raise AssertionError()
                ny += mv[0]
                nx += mv[1]

        max_goodness = 0
        max_y,max_x = None,None
        max_mv = None
        max_to = None
        for y in range(self.N):
            for x in range(self.N):
                # 何も置いてないかケーブルの場合はスキップ
                if self.field[y][x][0] == 0 or 6 <= self.field[y][x][0] <= 10:
                    continue
                for mv in [[0, 1], [1, 0]]:
                    canConnect,to = can_connect(y,x,mv)
                    if canConnect:
                        goodness = calc_goodness(y,x,mv)
                        if goodness > max_goodness:
                            max_goodness = goodness
                            max_y,max_x = y,x
                            max_mv = mv
                            max_to = to
        if max_goodness > 0:
            # print(max_goodness,max_y,max_x,max_mv,max_to)
            do_connect(max_y,max_x,max_mv,max_to)

        return

    def solve(self):
        
        lap_start = time.time()

        connects = set()
        moves = []
        while 1:
            # 接続されていないPCを有利な方向に1マス動かしてみる(移動とケーブル接続には2ターン必要)
            if len(moves) + len(connects) <= self.LIM-2:
                self._move(self.LIM-len(connects),moves,connects)
            # self.print_field()

            # 動かしたPCを接続してみる
            # 1回の移動につき何回接続を試みるかはパラメータで決定
            for _ in range(self.param):
                if len(moves) + len(connects) < self.LIM:
                    self._connect(self.LIM-len(moves), connects)

            # print_answer(Result(moves, connects))
            now = time.time()
            if now-lap_start >= 0.5 or now-self.start >= 2.75:
                return Result(moves, connects)

        return Result(moves, connects)

    def print_field(self):
        for y in range(self.N):
            tmp = []
            for x in range(self.N):
                tmp.append(self.field[y][x][0])
            print(tmp)

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1]*n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def unite(self, x, y):
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

# スコア計算用
def calc_score(N, K, field, res: Result):

    computers = defaultdict()
    cp_id = 0
    for y in range(N):
        for x in range(N):
            if field[y][x][0] != 0:
                computers[(y,x)] = [cp_id, field[y][x][0]]
                cp_id += 1

    for move in res.moves:
        y,x,ny,nx = move
        assert 1 <= field[y][x][0] <= K
        assert field[ny][nx][0] == 0
        field[ny][nx][0] = field[y][x][0]
        field[y][x][0] = 0
        computers[(ny,nx)] = computers[(y,x)][:]
        computers.pop((y,x))

    uf = UnionFind(K*100)
    for cn in res.connects:
        y,x,ny,nx = cn
        p1 = (y,x)
        p2 = (ny,nx)
        assert 1 <= field[y][x][0] <= K
        assert 1 <= field[ny][nx][0] <= K
        uf.unite(computers[p1][0],computers[p2][0])

    computers2 = [-1]*K*100
    for y in range(N):
        for x in range(N):
            if 1 <= field[y][x][0] <= K:
                id = computers[(y,x)][0]
                computers2[id] = (y,x)

    score = 0
    for i in range(K*100):
        for j in range(i+1, K*100):
            if uf.find(i) != uf.find(j):
                continue
            c1 = computers2[i]
            c2 = computers2[j]

            if field[c1[0]][c1[1]][0] == field[c2[0]][c2[1]][0]:
                score += 1
            else:
                score -= 1

    return max(score, 0)

def print_answer(res: Result):
    print(len(res.moves))
    for arr in res.moves:
        print(*arr)
    print(len(res.connects))
    for arr in res.connects:
        print(*arr)

def main():

    start = time.time()

    N,K = map(int,input().split())
    field = [[[] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        tmp = input()
        for j in range(N):
            field[i][j] = [int(tmp[j]),False,[-1,-1],[-1,-1]]

    # 時間いっぱいパラメータを変えてソルバーを回す
    best_result = Result([],[])
    best_score = 0
    connect_per_move = 2
    while 1:
        solver = Solver(N, K, deepcopy(field), start, connect_per_move)
        res = solver.solve()
        score = calc_score(N, K, deepcopy(field), res)
        # print(f"{score}", file=sys.stderr)
        # print(f"Remain={K*100-len(res.moves)-len(res.connects)}", file=sys.stderr)
        
        # 最大のスコアを保存
        if score > best_score:
            best_score = score
            best_result = res

        now = time.time()
        if now-start > 2.75:
            break

        # 1回の移動につき何回接続するかのパラメータを変更
        connect_per_move += 1

    print(f"{best_score}", file=sys.stderr)
    print_answer(best_result)

if __name__ == "__main__":
    main()
