import time
import random
from collections import namedtuple

DR = [1, 0, -1, 0]
DC = [0, 1, 0, -1]
DT = 5

# 乱数シミュレーション用のパラメータ
SIMU_LOOP_FIRST = 3 # 序盤のシミュレーション回数(0なら乱数シミュレーションしない)
PRUNE_NUM = 1 # 枝刈り後、終盤に回す候補数
SIMU_LOOP_LAST = 1 #終盤のシミュレーション
SWITCH_T_FIRST = 50 # 序盤の乱数シミュレーション開始ループ番号
SWITCH_T_MIDDLE = 150 # SWITCH_T_START～SWITCH_T_MIDDLEがSIMU_LOOP_FIRST回のシミュレーション対象
SWITCH_T_LAST = 800 # SWITCH_T_END～T=1000までがSIMU_LOOP_LAST回のシミュレーション対象
RAND_NUM = 2 # 機械の購入/移動場所の候補数(上位RAND_NUM個から乱数で選ぶ)
WEIGHT = (4,3) # 機械の購入/移動場所を決める際の重み
# RAND_NUM = 10 # 機械の購入/移動場所の候補数(上位RAND_NUM個から乱数で選ぶ)
# WEIGHT = (1,1,1,1,1,1,1,1,1,1) # 機械の購入/移動場所を決める際の重み

Vegetable = namedtuple('Vegetable', ['v', 'r', 'c', 's', 'e'])

class Action:
    def __init__(self, vs):
        self.vs = vs

    @classmethod
    def create_pass(cls):
        return cls([-1])

    @classmethod
    def create_purchase(cls, r, c):
        return cls([r, c])

    @classmethod
    def create_move(cls, r1, c1, r2, c2):
        return cls([r1, c1, r2, c2])

    def __str__(self):
        return " ".join(str(v) for v in self.vs)

class Game:
    def __init__(self, n, t, veges):
        self.n = n
        self.t = t
        self.machines = [] # 所持している機械の座標を格納
        self.has_machine = [[False]*n for _ in range(n)]
        self.next_price = 1
        self.num_machine = 0
        self.money = 1
        self.veges_start = [[] for _ in range(t)]  # veges_start[i] : vegetables appear on day i
        self.veges_end = [[] for _ in range(t)]    # veges_end[i] : vegetables disappear on day i
        self.future_value_total = [[[0]*n for _ in range(n)] for _ in range(t)] # 各t以降に各座標で将来収穫できる合計の収穫量
        self.future_value_total_around = [[[0]*n for _ in range(n)] for _ in range(t)] # 各t以降に各座標とその1マス周囲で将来収穫できる合計の収穫量
        self.veges_pos = [[[] for _ in range(n)] for _ in range(n)] # 各地点ごとに生える野菜のリスト
        for vege in veges:
            self.veges_start[vege.s].append(vege)
            self.veges_end[vege.e].append(vege)
            self.future_value_total[0][vege.r][vege.c] += vege.v
            for dr in range(-1,2):
                for dc in range(-1,2):
                    nr,nc = vege.r+dr,vege.c+dc
                    if 0 <= nr < n and 0 <= nc < n:
                        self.future_value_total_around[0][nr][nc] += vege.v
            self.veges_pos[vege.r][vege.c].append(vege)
        self.harvest_change = [[[0]*n for _ in range(n)] for _ in range(t)] # 各tにおける各座標の収穫量の推移
        self.harvest_change_around = [[[0]*n for _ in range(n)] for _ in range(t)] # 各tにおける各座標からマンハッタン距離が3以下のマスで収穫できる合計の収穫量
        for day in range(t):
            if day == 0:
                for vege in self.veges_start[day]:
                    self.harvest_change[day][vege.r][vege.c] += vege.v
            else:
                # まず前日の野菜の状態をコピー
                for r in range(n):
                    for c in range(n):
                        self.harvest_change[day][r][c] = self.harvest_change[day-1][r][c]
                        self.future_value_total[day][r][c] = self.future_value_total[day-1][r][c]
                        self.future_value_total_around[day][r][c] = self.future_value_total_around[day-1][r][c]

                # 生えた野菜、枯れた野菜の分を反映
                for vege in self.veges_start[day]:
                    self.harvest_change[day][vege.r][vege.c] += vege.v
                for vege in self.veges_end[day-1]:
                    self.harvest_change[day][vege.r][vege.c] -= vege.v
                    self.future_value_total[day][vege.r][vege.c] -= vege.v
                    for dr in range(-1,2):
                        for dc in range(-1,2):
                            nr,nc = vege.r+dr,vege.c+dc
                            if 0 <= nr < n and 0 <= nc < n:
                                self.future_value_total_around[day][nr][nc] -= vege.v

            # 各tにおける各座標からマンハッタン距離が3以下のマスで収穫できる合計の収穫量をスコア化
            for r in range(n):
                for c in range(n):
                    if self.harvest_change[day][r][c] == 0:
                        continue
                    cnt = 0
                    for dr in range(-3,4):
                        for dc in range(-3,4):
                            nr,nc = r+dr,c+dc
                            if 0 <= nr < n and 0 <= nc < n and abs(nr-r)+abs(nc-c) <= 3 and self.harvest_change[day][nr][nc] > 0:
                                cnt += 1
                    self.harvest_change_around[day][r][c] += self.harvest_change[day][r][c] * cnt

        self.connected_harvest = [[[0]*n for _ in range(n)] for _ in range(t)] # 各tにおいて周囲の野菜との連結度で重み付けした野菜の収穫量
        for day in range(t):
            visited = [set([]) for _ in range(DT)]
            for r in range(n):
                for c in range(n):
                    for dt in range(DT):
                        if day+dt == self.t or self.harvest_change[min(self.t-1, day+dt)][r][c] == 0:
                            break
                        queue = [(r, c)]
                        visited[dt].add((r,c))
                        if dt == 0:
                            self.connected_harvest[day][r][c] += self.harvest_change[min(self.t-1, day+dt)][r][c]
                        i = 0
                        while i < len(queue):
                            cr, cc = queue[i]
                            for dir in range(4):
                                nr = cr + DR[dir]
                                nc = cc + DC[dir]
                                if 0 <= nr < self.n and 0 <= nc < self.n and self.harvest_change[min(self.t-1, day+dt)][nr][nc] > 0 and (nr,nc) not in visited[dt]:
                                    visited[dt].add((nr,nc))
                                    queue.append((nr, nc))
                                    self.connected_harvest[day][r][c] += self.harvest_change[min(self.t-1, day+dt)][nr][nc]
                            i += 1

        # for i in range(5):
        #     for t in self.harvest_change_around_total[i]:
        #         print(*t)
        #     print("\n")

    def purchase(self, r, c):
        assert not self.has_machine[r][c]
        assert self.next_price <= self.money
        self.machines.append([r,c]) # machineの追加
        self.has_machine[r][c] = True
        self.num_machine += 1
        self.money -= self.next_price
        self.next_price = (self.num_machine + 1) ** 3

    def move(self, r1, c1, r2, c2):
        for i,machine in enumerate(self.machines):
            if [r1,c1] == machine:
                self.machines[i] = [r2, c2] # machineの移動
        assert self.has_machine[r1][c1]
        self.has_machine[r1][c1] = False
        assert not self.has_machine[r2][c2]
        self.has_machine[r2][c2] = True

    def simulate(self, day, action):
        # apply
        if len(action.vs) == 2:
            self.purchase(*action.vs)
        elif len(action.vs) == 4:
            self.move(*action.vs)
        # harvest
        for r in range(self.n):
            for c in range(self.n):
                if self.has_machine[r][c] and self.harvest_change[day][r][c] > 0:
                    self.money += self.harvest_change[day][r][c] * self.count_connected_machines(r,c)
                    # 収穫した地点に関して、harvest_changeの該当する期間の野菜の価値を0にする
                    end = -1
                    for vege in self.veges_pos[r][c]:
                        if vege.s <= day <= vege.e:
                            end = vege.e + 1
                            break
                    for i in range(day,end):
                        self.harvest_change[i][r][c] = 0

    def count_connected_machines(self, r, c):
        queue = [(r, c)]
        visited = [[False] * self.n for _ in range(self.n)]
        visited[r][c] = True
        i = 0
        while i < len(queue):
            cr, cc = queue[i]
            for dir in range(4):
                nr = cr + DR[dir]
                nc = cc + DC[dir]
                if 0 <= nr < self.n and 0 <= nc < self.n and self.has_machine[nr][nc] and not visited[nr][nc]:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
            i += 1
        return i

    # 機械の移動元、移動先を決定
    def search_machine_move(self, day, rand_flg):
        move_before = [-1,-1]
        move_after = [-1,-1]

        # 各機械を移動対象とした時に、移動先として直近の未来で収穫量が最大となる地点を他の機械の周囲で探索
        if self.num_machine == 1:
                move_before = self.machines[0]
                move_after, _ = self.search_max_pos_move(day, rand_flg, move_before)
        elif self.num_machine <= 3:
            max_harvest = 0
            # 動かす機械を全探索
            for machine1 in self.machines:
                r1,c1 = machine1
                # 移動先で隣接させる機械と移動先の座標を探索
                for machine2 in self.machines:
                    if machine1 == machine2:
                        continue
                    r2,c2 = machine2
                    for dir in range(4):
                        nr,nc = r2+DR[dir],c2+DC[dir]
                        if 0 <= nr < self.n and 0 <= nc < self.n and not self.has_machine[nr][nc] and self.harvest_change[day][nr][nc] > 0:
                            self.move(r1,c1,nr,nc)
                            harvest = self.harvest_change_around[day][nr][nc] * self.count_connected_machines(nr,nc)
                            self.move(nr,nc,r1,c1)
                            if harvest > max_harvest:
                                max_harvest = harvest
                                move_before = machine1
                                move_after = [nr,nc]
                # 隣接させずに独立して移動させたほうがよいか判定
                move_after2, max_harvest2 = self.search_max_pos_move(day, rand_flg, machine1)
                if max_harvest2 > max_harvest:
                    move_before = machine1
                    move_after = move_after2
        else:
            # 動かす機械
            min_harvest = 10**18
            # 将来的な見込み収穫量が最も少ない機械を探索
            for machine in self.machines:
                r1,c1 = machine
                harvest = self.harvest_change[day][r1][c1] * self.count_connected_machines(r1,c1)
                if harvest < min_harvest:
                    min_harvest = harvest
                    move_before = [r1,c1]

            # 移動先で隣接させる機械と移動先の座標を探索
            move_after, _ = self.search_max_pos_move(day, rand_flg, move_before)

        if move_before != [-1,-1] and move_after != [-1,-1]:
            return [*move_before, *move_after]
        else:
            return [-1,-1,-1,-1]

    # 機械の移動先を探索
    def search_max_pos_move(self, day, rand_flg, move_before=[-1,-1]):
        pos_list = []
        future = day
        while future < min(self.t, day+10):
            for r in range(self.n):
                for c in range(self.n):
                    if self.has_machine[r][c] or self.harvest_change[day][r][c] == 0:
                        continue
                    # 連結も考慮した収穫量計算
                    if move_before != [-1,-1]:
                        self.move(*move_before,r,c)
                        harvest = self.harvest_change_around[future][r][c] * self.count_connected_machines(r,c)
                        self.move(r,c,*move_before)
                    else:
                        harvest = self.harvest_change_around[future][r][c] * self.count_connected_machines(r,c)
                    pos_list.append([harvest, (r,c)])
            if len(pos_list) > 0:
                break
            future += 1

        # 乱数を使うかどうか
        if len(pos_list):
            pos_list.sort(reverse=True)
            if rand_flg:
                len_pos = min(RAND_NUM, len(pos_list))
                pos = random.choices(pos_list[:len_pos],k=1,weights=WEIGHT[:len_pos])
                return pos[0][1], pos[0][0]
            else:
                return pos_list[0][1], pos_list[0][0]
        else:
            return [-1,-1], 0

    # 機械の購入場所を探索
    def search_max_pos_purchase(self, day, rand_flg):
        pos_list = []
        for r in range(self.n):
            for c in range(self.n):
                if self.has_machine[r][c]:# or (self.num_machine <= 1 and self.harvest_change[day][r][c] == 0):
                    continue
                # 今後最も高い収穫量を見込める位置
                harvest = self.future_value_total_around[day][r][c] * self.count_connected_machines(r,c)
                pos_list.append([harvest, (r,c)])

        # 乱数を使うかどうか
        if len(pos_list):
            pos_list.sort(reverse=True)
            if rand_flg:
                len_pos = min(RAND_NUM, len(pos_list))
                pos = random.choices(pos_list[:len_pos],k=1,weights=WEIGHT[:len_pos])
                return pos[0][1], pos[0][0]
            else:
                return pos_list[0][1], pos_list[0][0]
        else:
            return [-1,-1], 0

    def select_next_action(self, day, rand_flg=False):
        # 機械の購入資金があるかないか
        if self.money < self.next_price:
            # ない場合、既にある機械のうち直近の見込み収穫量が最も少ないものを、より野菜が収穫できる座標へ移動させる
            move = self.search_machine_move(day,rand_flg)
            
            if move != [-1,-1,-1,-1]:
                return Action.create_move(*move)
            else:
                return Action.create_pass()
        else:
            # 機械を購入する場合は、将来的に最も高い収穫量を見込める座標を探索
            purchase_pos, _ = self.search_max_pos_purchase(day,rand_flg)

            # ループの終盤では機械を購入できなくする
            if purchase_pos != [-1,-1] and day < 850:
                return Action.create_purchase(*purchase_pos)
            else:
                move = self.search_machine_move(day,rand_flg)
                if move != [-1,-1,-1,-1]:
                    return Action.create_move(*move)
                else:
                    return Action.create_pass()


def main():

    # タイム計測開始
    start = time.time()

    N, M, T = list(map(int, input().split()))
    veges = []
    for _ in range(M):
        r, c, s, e, v = list(map(int, input().split()))
        veges.append(Vegetable(v, r, c, s, e))

    game = Game(N, T, veges)

    actions = []
    rand_flg = False
    # 乱数を使う場合
    if SIMU_LOOP_FIRST > 0:        
        # 最序盤は乱数なし
        for day in range(SWITCH_T_FIRST):
            action = game.select_next_action(day,rand_flg)
            actions.append([*action.vs])
            game.simulate(day, action)
        
        # 最序盤終了時のパラメータのコピー
        copy_machines = [[machine[0],machine[1]] for machine in game.machines]
        copy_has_machine = [[False]*N for _ in range(N)]
        copy_harvest_change = [[[0]*N for _ in range(N)] for _ in range(T)]
        for day in range(SWITCH_T_FIRST,T):
            for r in range(N):
                for c in range(N):
                    if day == SWITCH_T_FIRST:
                        copy_has_machine[r][c] = game.has_machine[r][c]
                    copy_harvest_change[day][r][c] = game.harvest_change[day][r][c]
        copy_next_price = game.next_price
        copy_num_machine = game.num_machine
        copy_money = game.money

        # 序盤の乱数シミュレーション
        candidate_actions_first = []
        parameters_first = []
        for i in range(SIMU_LOOP_FIRST+1):
            # 最初の1回はランダム性無し、以降SIMU_LOOP回はランダム性あり
            if i > 0:
                rand_flg = True

            tmp_actions = [[*action.vs] for action.vs in actions]            
            # 序盤シミュレーション実行
            for day in range(SWITCH_T_FIRST, SWITCH_T_MIDDLE):
                action = game.select_next_action(day,rand_flg)
                tmp_actions.append([*action.vs])
                game.simulate(day, action)

            # 序盤終了時のパラメータのコピー
            candidate_actions_first.append([game.money, tmp_actions])
            tmp_parameter = []
            tmp_has_machine = [[False]*N for _ in range(N)]
            tmp_harvest_change = [[[0]*N for _ in range(N)] for _ in range(T)]
            for day in range(SWITCH_T_FIRST,T):
                for r in range(N):
                    for c in range(N):
                        if day == SWITCH_T_FIRST:
                            tmp_has_machine[r][c] = game.has_machine[r][c]
                        tmp_harvest_change[day][r][c] = game.harvest_change[day][r][c]
            tmp_parameter.append([[machine[0],machine[1]] for machine in game.machines])
            tmp_parameter.append(tmp_has_machine)
            tmp_parameter.append(tmp_harvest_change)
            tmp_parameter.append(game.next_price)
            tmp_parameter.append(game.num_machine)
            tmp_parameter.append(game.money)
            parameters_first.append(tmp_parameter)

            # 次のループ用にgameのインスタンス変数を初期化
            game.machines = [[machine[0],machine[1]] for machine in copy_machines]
            for day in range(SWITCH_T_FIRST,T):
                for r in range(N):
                    for c in range(N):
                        if day == SWITCH_T_FIRST:
                            game.has_machine[r][c] = copy_has_machine[r][c]
                        game.harvest_change[day][r][c] = copy_harvest_change[day][r][c]
            game.next_price = copy_next_price
            game.num_machine = copy_num_machine
            game.money = copy_money

        # print([candidate_actions_first[i][0] for i in range(len(candidate_actions_first))])

        # 序盤の乱数シミュレーション結果から乱数無し版と、乱数あり版の上位PRUNE_NUM個を選定
        candidate_actions_middle = []
        parameters_middle = []
        candidate_actions_middle.append(candidate_actions_first[0])
        parameters_middle.append(parameters_first[0])
        moneys = sorted([candidate_actions_first[i+1][0] for i in range(SIMU_LOOP_FIRST)], reverse=True)[:PRUNE_NUM]
        for i in range(PRUNE_NUM):
            target_money = moneys[i]
            for j in range(1,SIMU_LOOP_FIRST+1):
                if candidate_actions_first[j][0] == target_money:
                    tmp_actions = [candidate_actions_first[j][0], [[*action.vs] for action.vs in candidate_actions_first[j][1]]]
                    candidate_actions_middle.append(tmp_actions)
                    tmp_parameter = []
                    tmp_has_machine = [[False]*N for _ in range(N)]
                    tmp_harvest_change = [[[0]*N for _ in range(N)] for _ in range(T)]
                    for day in range(SWITCH_T_FIRST,T):
                        for r in range(N):
                            for c in range(N):
                                if day == SWITCH_T_FIRST:
                                    tmp_has_machine[r][c] = parameters_first[j][1][r][c]
                                tmp_harvest_change[day][r][c] = parameters_first[j][2][day][r][c]
                    tmp_parameter.append([[machine[0],machine[1]] for machine in parameters_first[j][0]])
                    tmp_parameter.append(tmp_has_machine)
                    tmp_parameter.append(tmp_harvest_change)
                    tmp_parameter.append(parameters_first[j][3])
                    tmp_parameter.append(parameters_first[j][4])
                    tmp_parameter.append(parameters_first[j][5])
                    parameters_middle.append(tmp_parameter)
                    candidate_actions_first[j][0] = -1

        # print([candidate_actions_middle[i][0] for i in range(len(candidate_actions_middle))])

        # 中盤は乱数無しで普通に処理
        rand_flg = False
        for i in range(PRUNE_NUM+1):
            # 序盤終了時パラメータの復元
            game.machines = [[machine[0],machine[1]] for machine in parameters_middle[i][0]]
            for day in range(SWITCH_T_MIDDLE,T):
                for r in range(N):
                    for c in range(N):
                        if day == SWITCH_T_MIDDLE:
                            game.has_machine[r][c] = parameters_middle[i][1][r][c]
                        game.harvest_change[day][r][c] = parameters_middle[i][2][day][r][c]
            game.next_price = parameters_middle[i][3]
            game.num_machine = parameters_middle[i][4]
            game.money = parameters_middle[i][5]

            # 中盤シミュレーション実行
            for day in range(SWITCH_T_MIDDLE, SWITCH_T_LAST):
                action = game.select_next_action(day,rand_flg)
                candidate_actions_middle[i][1].append([*action.vs])
                game.simulate(day, action)
            
            # 中盤終了時のパラメータのコピー
            candidate_actions_middle[i][0] = game.money
            parameters_middle[i][0] = [[machine[0],machine[1]] for machine in game.machines]
            for day in range(SWITCH_T_LAST,T):
                for r in range(N):
                    for c in range(N):
                        if day == SWITCH_T_LAST:
                            parameters_middle[i][1][r][c] = game.has_machine[r][c]
                        parameters_middle[i][2][day][r][c] = game.harvest_change[day][r][c]
            parameters_middle[i][3] = game.next_price
            parameters_middle[i][4] = game.num_machine
            parameters_middle[i][5] = game.money

        # 終盤の乱数シミュレーション
        candidate_actions_last = []
        if SWITCH_T_LAST < T:
            # 枝刈りされた中盤までのシミュレーション結果のそれぞれに対して終盤シミュレーション実施
            for i in range(PRUNE_NUM+1):
                # 中盤までの各シミュレーション結果のそれぞれに対して、終盤に1回は乱数なしのパターンを用意
                rand_flg = False
                for j in range(SIMU_LOOP_LAST+1):
                    # 中盤終了時パラメータの復元
                    copy_actions = [[*action.vs] for action.vs in candidate_actions_middle[i][1]]
                    game.machines = [[machine[0],machine[1]] for machine in parameters_middle[i][0]]
                    for day in range(SWITCH_T_LAST,T):
                        for r in range(N):
                            for c in range(N):
                                if day == SWITCH_T_LAST:
                                    game.has_machine[r][c] = parameters_middle[i][1][r][c]
                                game.harvest_change[day][r][c] = parameters_middle[i][2][day][r][c]
                    game.next_price = parameters_middle[i][3]
                    game.num_machine = parameters_middle[i][4]
                    game.money = parameters_middle[i][5]

                    # 最初の1回はランダム性無し、以降SIMU_LOOP回はランダム性あり
                    if j > 0:
                        rand_flg = True

                    # 終盤シミュレーション実行
                    for day in range(SWITCH_T_LAST, T):
                        action = game.select_next_action(day,rand_flg)
                        copy_actions.append([*action.vs])
                        game.simulate(day, action)

                    # 最終シミュレーション結果のコピー
                    candidate_actions_last.append([[game.money], [[*action.vs] for action.vs in copy_actions]])

                    # 制限時間ギリギリならループを抜ける(TLE対策)
                    now = time.time()
                    if i > 0 and now-start > 1.8:
                        break

            # print(sorted([candidate_actions_last[i][0] for i in range(len(candidate_actions_last))], reverse=True))

            # シミュレーション結果で最善のものを出力
            max_money = sorted([candidate_actions_last[i][0] for i in range(len(candidate_actions_last))], reverse=True)[0]
            for candidate_actions in candidate_actions_last:
                if candidate_actions[0] == max_money:
                    actions = candidate_actions[1]
                    break

        else:
            # 終盤の乱数シミュレーションをしない場合
            for i in range(PRUNE_NUM+1):
                # 中盤盤終了時パラメータの復元
                game.machines = [[machine[0],machine[1]] for machine in parameters_middle[i][0]]
                for day in range(SWITCH_T_LAST,T):
                    for r in range(N):
                        for c in range(N):
                            if day == SWITCH_T_LAST:
                                game.has_machine[r][c] = parameters_middle[i][1][r][c]
                            game.harvest_change[day][r][c] = parameters_middle[i][2][day][r][c]
                game.next_price = parameters_middle[i][3]
                game.num_machine = parameters_middle[i][4]
                game.money = parameters_middle[i][5]

                # 終盤シミュレーション実行
                for day in range(SWITCH_T_LAST,T):
                    action = game.select_next_action(day,rand_flg)
                    candidate_actions_middle[i][1].append([*action.vs])
                    game.simulate(day, action)
                
                # シミュレーション結果のコピー
                candidate_actions_middle[i][0] = game.money
            
            # シミュレーション結果で最善のものを出力
            max_money = sorted([candidate_actions_middle[i][0] for i in range(len(candidate_actions_middle))], reverse=True)[0]
            for candidate_actions in candidate_actions_middle:
                if candidate_actions[0] == max_money:
                    actions = candidate_actions[1]
                    break
    else:
        # 乱数シミュレーションをしない場合
        for day in range(T):
            action = game.select_next_action(day,rand_flg)
            actions.append([*action.vs])
            game.simulate(day, action)

    for action in actions:
        print(*action)

if __name__ == '__main__':
    main()
