from dataclasses import dataclass
from typing import List
from heapq import heappush, heappop
import time
import sys,pypyjit
input = lambda: sys.stdin.readline().rstrip()
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

### CONST ###
INF = 10**18
TIME_LIMIT = 2.5
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
MOVE_AROUND = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動

INI_SWITCH_M = 2 # 初期方針を切り替えるMの閾値
FORECAST_INTERVAL = 2 # ポリオミノの形そのままで占う時の間隔
RESEARCH_TOP_K = 3 # ポリオミノの形そのままで占った結果、v(S)上位何個に対し隣接マスを再調査するか
FORECAST_LEN = 3 # 占う正方形領域の一辺の長さ
TRIAL_DIG_SWITCH_RATIO = 0.75 # 全油田量の何割が掘れたら試し掘り方式の判定ロジックを変えるかの閾値
TRIAL_DIG_SWITCH_RATIO2 = 0.6 # 全油田量の何割が掘れたら試し掘り方式の判定ロジックを変えるかの閾値2
TRIAL_DIG_SWITCH_TURN = 140 # 試し掘り方式からBFSでの隣接マス発掘方式に切り替えるターン
TRIAL_DIG_NUM = 4 # 1ターンで何回試し掘りするか
TRIAL_DIG_CAND_NUM = 10 # 毎回の試し掘り場所決めの候補とする座標の数
DIST_WEIGHT = 2.5 # 試し掘りの候補マスの隣接マスにv(y,x)>0のマスがある場合の重み
DFS_LIMIT = 3 * 10**6
MIN_FORECAST_OIL_RATIO = 0.05 # 全油田量の何割が掘れていないと占えないようにするかの閾値

@dataclass
class OIL:
    """油田クラス
    Note:
        各油田が持つマス数とその座標を持つ
    Attributes
        n (int): 油田が持つマス数
        pos (List[List[int]]): 油田に含まれる各点の座標
        relative_pos (List[List[int]]): 1点目の座標を基準にした時の残りの座標の相対位置
    """
    n: int
    pos_list: List[List[int]]
    relative_pos_list: List[List[int]]

class Judge:
    """ジャッジクラス
    Note:
        ジャッジとのやり取りを管理
    """
    def __init__(self, n: int, m: int, eps: float, oils: List[OIL]):
        self.N = n
        self.M = m
        self.EPS = eps
        self.OILS = oils

        self.turn = 0
        self.turn_limit = 2 * n**2
        self.cost = 0
        self.forecasted_poly_set = [set() for _ in range(self.M)] # 各ポリオミノの形状で占い済の(base_y,base_x)一覧
        self.digged_total_pos_set = set() # これまでに発掘した場所
        self.digged_oil_pos_set = set() # これまでに発掘した油田がある場所
        self.digged_oil_amount = 0 # これまでに発掘された総油田量
        self.definitive_oil_pos_set = set() # 発掘していないが油田があると確定した場所
        self.definitive_poly_id = set() # 配置が確定したポリオミノのID
        self.answered_pos_tuple = set() # これまで回答したソート済み座標タプルの集合

        # フィールド管理用変数
        self.oil_map = [[-1]*n for _ in range(n)] # 確定した油田の埋蔵量の地図(-1:不明、0以上：確定)
        self.oil_forecast_map = [[-1.0]*n for _ in range(n)] # マスごとの予想埋蔵量
        self.possible_poly_pos_map = [[set() for _ in range(n)] for _ in range(n)] # そのマスにそのidのポリオミノが存在できるか(掘る度更新)
        self.initialize_possible_poly_map()
        self.definitive_poly_pos_map = [[set() for _ in range(n)] for _ in range(n)] # 発掘の結果を基に確定したポリオミノの配置

    def dig_pos(self, y: int, x: int) -> int:
        """任意の1マスを掘る
        Args:
            y (int): 掘るマスのy座標
            x (int): 掘るマスのx座標
        """
        if self.turn == self.turn_limit:
            return -1

        req = ["q", 1, y, x]
        print(*req, flush=True)

        self.turn += 1
        self.cost += 1
        actual_oil_amount = int(input())

        # 発掘済み座標セットに追加
        self.digged_total_pos_set.add((y,x))
        if actual_oil_amount > 0:
            self.digged_oil_pos_set.add((y,x))
            # (y,x)の発掘が初めてかつv(S)>0なら発掘済み油田量に加算
            if self.oil_map[y][x] != actual_oil_amount:
                self.digged_oil_amount += actual_oil_amount

        self.oil_map[y][x] = actual_oil_amount
        self.update_possible_poly_map()
        return actual_oil_amount

    def initialize_possible_poly_map(self) -> None:
        """初期状態で各ポリオミノが存在できるマスの(base_y,base_x)情報を管理
        """
        for poly_id,oil in enumerate(self.OILS):
            for base_y in range(self.N):
                for base_x in range(self.N):
                    failure_flg = False
                    # 範囲外に出てしまうポリオミノの配置は駄目
                    for dy,dx in oil.relative_pos_list:
                        ny,nx = base_y+dy,base_x+dx
                        if not (0<=ny<self.N and 0<=nx<self.N):
                            failure_flg = True
                            break
                    if failure_flg:
                        continue
                    self.possible_poly_pos_map[base_y][base_x].add(poly_id)

    def update_possible_poly_map(self) -> None:
        """掘る度に各ポリオミノが存在できるマスの情報を更新
        """
        for poly_id,oil in enumerate(self.OILS):
            for base_y in range(self.N):
                for base_x in range(self.N):
                    failure_flg = False
                    for dy,dx in oil.relative_pos_list:
                        ny,nx = base_y+dy,base_x+dx
                        if not (0<=ny<self.N and 0<=nx<self.N):
                            failure_flg = True
                            break
                        # 埋蔵量が0に確定した座標を含むポリオミノは置けない
                        if self.oil_map[ny][nx] == 0:
                            failure_flg = True
                            break
                        # 試し掘りで配置が確定したポリオミノがある地点にも置けない
                        if self.oil_map[ny][nx] > 0 and len(self.definitive_poly_pos_map[ny][nx]) == self.oil_map[ny][nx] and poly_id not in self.definitive_poly_pos_map[ny][nx]:
                            failure_flg = True
                            break
                    if failure_flg:
                        if poly_id in self.possible_poly_pos_map[base_y][base_x]:
                            self.possible_poly_pos_map[base_y][base_x].remove(poly_id)
                        continue

    def forecast_pos_list(self, pos_list: list[list[int]]) -> int:
        """指定したマスの集合が持つ石油埋蔵量を占う

        Args:
            pos (list[list[int]): 占う対象のマスのリスト
        """
        if self.turn == self.turn_limit:
            return -1

        assert len(pos_list) >= 2 # 占うマスは2マス以上必要

        req = ["q"]
        req.append(len(pos_list))
        for y,x in pos_list:
            req.append(y)
            req.append(x)
        
        print(*req, flush=True)

        self.turn += 1
        self.cost += 1 / (len(pos_list))**0.5
        v_S = int(input())
        each_v_S =  v_S / len(pos_list)

        # 占った座標リストにv(S)を分配
        for y,x in pos_list:
            if self.oil_forecast_map[y][x] == -1.0:
                self.oil_forecast_map[y][x] = each_v_S
            else:
                self.oil_forecast_map[y][x] = (self.oil_forecast_map[y][x] + each_v_S)/2

        return v_S
    
    def answer(self, pos_set: set) -> int:
        """見つかった全ての油田の座標を出力
        """
        if self.turn == self.turn_limit:
            return 0
        
        # 一度でも回答したことのある座標の組合せは受け付けない
        sorted_pos_tuple = tuple(sorted(list(pos_set)))
        if sorted_pos_tuple in self.answered_pos_tuple:
            print("#c same answer in past", file=sys.stderr)
            return 0

        req = ["a", len(pos_set)]
        for y,x in pos_set:
            req.append(y)
            req.append(x)

        print(*req, flush=True)

        self.turn += 1
        res = int(input())
        return res

    def debug(self, message: str = "") -> None:
        """デバッグ用コメントを出力
        """
        # print(f"#c {message}")
        print(f"#c turn = {str(self.turn)}")
        print(f"#c cost = {str(self.cost)}")
        print(f"#c digged_oil_amount = {self.digged_oil_amount}")


class Solver:
    """ソルバクラス
    Note:
        解法を記載するクラス
    Attributes
        N (int): 島の一辺の長さ
        M (int): 島に含まれる油田の個数
        EPS (int): 占い時の誤差の大きさ
        OILS (List[OIL]): 油田のマス数及び左上に寄せた時の座標
    """
    def __init__(self, n: int, m: int, eps: float, oils: List[OIL]):
        self.start_time = time.time()
        self.current_time = time.time()
        self.N = n
        self.M = m
        self.EPS = eps
        self.OILS = oils
        self.calc_oil_relative_pos()
        self.judge = Judge(n,m,eps,oils)

        self.cost = 0
        self.score = 0
        self.total_oil_amount = sum([oil.n for oil in oils]) # 埋蔵されている全油田量
        self.high_v_S_pos_hq = [] # 占い結果の推定v(S)が高い順に格納された座標リスト
        self.trial_dig_cand_pos_list = [] # 試し掘り候補の座標管理用リスト

    def solve(self) -> int:

        # 1. Mの大小によって初期方針を変える
        if self.M <= INI_SWITCH_M:
            # 1-1. Mが2の時はポリオミノの形そのままにスライドさせて最もv(S)が大きくなったところを解とする
            oil_pos_set = self.slide_optimal_oil_pos()
            if oil_pos_set:
                finish_flg = self.judge.answer(oil_pos_set)
                if finish_flg:
                    return
        else:
            # 1-2. N*Nの島全体をFORECAST_LEN*FORECAST_LENのグループに区切ってそれぞれの埋蔵量を占う
            self.forecast_all_group(FORECAST_LEN,1)
            if self.judge_if_turn_over():
                return

        # 2. 未占いマスを隣接マスの値の平均で補間
        self.interpolate_unforecast_v_S()

        # 3. 占い結果の全座標を推定v(S)が高い順になるように管理する。
        self.create_sorted_pos_list()

        # 4. 試し掘りと隣接マス発掘を繰り返す
        while 1:
            # 上限ターンに達するか全ての埋蔵石油が発掘できたら終了
            if self.judge_if_turn_over() or self.judge_if_digged_all():
                break

            # TLE対策
            self.current_time = time.time()
            if self.current_time - self.start_time >= TIME_LIMIT:
                break

            # 4. DFSで最適な配置を探索する
            # 4-1. 確定情報を増やすために試し掘りする
            if len(self.judge.digged_oil_pos_set | self.judge.definitive_oil_pos_set) < self.total_oil_amount * TRIAL_DIG_SWITCH_RATIO and self.judge.turn < TRIAL_DIG_SWITCH_TURN:
                self.trial_dig()
            else:
                self.dig_adjacent_pos()
                if self.judge_if_turn_over() or self.judge_if_digged_all():
                    break

            # 4-2. 現時点の情報を基に、最適な配置を探索し回答する
            oil_pos_set = self.find_optimal_arrangement()
            # 全油田量の一定割合以上が座標確定できていない場合は占わない
            if oil_pos_set and len(self.judge.digged_oil_pos_set | self.judge.definitive_oil_pos_set) > self.total_oil_amount * MIN_FORECAST_OIL_RATIO:
                finish_flg = self.judge.answer(oil_pos_set)
                if finish_flg:
                    return

        # 5. ここまでに回答できていなければ全ての油田を発掘して答えを出力する
        while not (self.judge_if_turn_over() or self.judge_if_digged_all()):
            self.dig_adjacent_pos()

        if not self.judge_if_turn_over():
            self.judge.answer(self.judge.digged_oil_pos_set | self.judge.definitive_oil_pos_set)
        return

    def slide_optimal_oil_pos(self):
        """島全体に対し、各油田(ポリオミノ)の形状そのままスライドさせて占い、最もv(S)が大きい場所を解とする。
        """
        # 内部関数
        def _calc_forecast_pos_list(base_y,base_x,oil):
            """当該油田ポリオミノの全マスが島の範囲内に存在するか判定し座標リストを返す。
            """
            forecast_pos_list = []
            for dy,dx in oil.relative_pos_list:
                ny,nx = base_y+dy,base_x+dx
                if not (0<=ny<self.N and 0<=nx<self.N):
                    return []
                forecast_pos_list.append((ny,nx))
            return forecast_pos_list

        def _judge_if_skip(forecast_pos_list):
            """これまでの占い結果をもとに今回占うポリオミノの領域の推定v(S)が小さそうならスキップする。
            """
            estimated_v_S = 0
            cnt_not_updated = 0 # 初期値(-1.0)のまま更新されていない未発掘マスの数
            for y,x in forecast_pos_list:
                if self.judge.oil_forecast_map[y][x] == -1.0:
                    cnt_not_updated += 1
                else:
                    estimated_v_S += self.judge.oil_forecast_map[y][x]
            
            # 初期値のままのマスが多い場合は未知数のため占う(スキップしない)
            if cnt_not_updated > len(forecast_pos_list) // 2.5:
                return False

            # 推定v(S)が閾値より小さかったら占う価値なし
            if estimated_v_S < 0.2 * len(forecast_pos_list):
                return True

        def _forecast_and_update(i,oil,forecast_pos_list,max_v_S,best_oil_pos_list):
            """当該油田ポリオミノの全マスが島の範囲内に存在する場合、占いを実行し最適油田位置を更新する。
            """
            v_S = -1
            if len(forecast_pos_list) != oil.n:
                return v_S
            v_S = self.judge.forecast_pos_list(forecast_pos_list)
            # 上限ターンに達したら終了
            if self.judge_if_turn_over():
                return -1
            if v_S > max_v_S[i]:
                max_v_S[i] = v_S
                best_oil_pos_list[i] = forecast_pos_list
            return v_S

        # メイン処理
        max_v_S = [0]*self.M
        best_oil_pos_list = [[] for _ in range(self.M)]
        oil_pos_set = set() # 回答用の座標セット格納変数

        # 最初にFORECAST_INTERVALだけ間隔を空けて占い、付近に油田がありそうなマスを再度占うためにv(S)を保存する
        research_pos_list = [[] for _ in range(self.M)] # (v(S), (y,x))
        forecasted_pos_set = [set() for _ in range(self.M)]
        for i,oil in enumerate(self.OILS):
            for gr_y in range(self.N//FORECAST_INTERVAL):
                for gr_x in range(self.N//FORECAST_INTERVAL):
                    base_y,base_x = gr_y*FORECAST_INTERVAL, gr_x*FORECAST_INTERVAL

                    forecast_pos_list = _calc_forecast_pos_list(base_y,base_x,oil)
                    # これまでの占い結果をもとに今回占うポリオミノの領域のv(S)が小さそうならスキップ(最初のポリオミノは必ず占う)
                    if i > 0 and _judge_if_skip(forecast_pos_list):
                        continue

                    v_S = _forecast_and_update(i,oil,forecast_pos_list,max_v_S,best_oil_pos_list)
                    forecasted_pos_set[i].add((base_y,base_x))
                    # 上限ターンに達したら終了
                    if self.judge_if_turn_over():
                        return
                    # v(S)が大きいマスは付近に油田がある可能性が高いため再占いのために保存
                    research_pos_list[i].append((v_S, (base_y,base_x)))

        # 付近に油田がある可能性が高いマス周辺を再占い
        for i,oil in enumerate(self.OILS):
            research_pos_list[i].sort(reverse=True)
            for j in range(min(len(research_pos_list[i]),RESEARCH_TOP_K)):
                base_y,base_x = research_pos_list[i][j][1]
                for dy,dx in MOVE_AROUND:
                    ny,nx = base_y+dy, base_x+dx
                    if (ny,nx) in forecasted_pos_set[i]:
                        continue
                    forecast_pos_list = _calc_forecast_pos_list(ny,nx,oil)
                    _forecast_and_update(i,oil,forecast_pos_list,max_v_S,best_oil_pos_list)
                    forecasted_pos_set[i].add((ny,nx))
                    # 上限ターンに達したら終了
                    if self.judge_if_turn_over():
                        return oil_pos_set
                    
        # スライドして見つけた油田の位置を回答
        for oil_pos_list in best_oil_pos_list:
            oil_pos_set |= set(oil_pos_list)

        return oil_pos_set

    def forecast_all_group(self, forecast_len, shift_num) -> None:
        """N*Nの島全体をFORECAST_LEN*FORECAST_LENの座標グループに区切ってそれぞれの埋蔵量を占う
        """
        # 島全体をFORECAST_LEN*FORECAST_LENの区画に分けて占う
        min_poly_size = min([oil.n for oil in self.OILS])
        forecast_len = max(FORECAST_LEN, min(4,min_poly_size//4))
        forecast_group_len = -(-(self.N)//forecast_len) # 島の一辺(N)をFORECASTで割った時のceil
        # TODO: 全油田マスが見つかったと思われる時は打ち切り
        # より正確なv(S)が測れるように1マスずつ縦横をずらして2回測定も可能(やらない方がスコア高い)
        for diff in range(shift_num):
            for gr_y in range(forecast_group_len):
                for gr_x in range(forecast_group_len):
                    pos_list = []
                    for dy in range(forecast_len):
                        for dx in range(forecast_len):
                            y,x = forecast_len * gr_y + dy + diff, forecast_len * gr_x + dx + diff
                            if not (0<=y<self.N and 0<=x<self.N):
                                continue
                            pos_list.append((y,x))
                    # 占うためには2マス以上必要
                    if len(pos_list) >= 2:
                        self.judge.forecast_pos_list(pos_list)
                        # 上限ターンに達したら終了
                        if self.judge_if_turn_over():
                            return

    def trial_dig(self) -> None:
        """油田が見つかる可能性が高いマスをいくつか試し掘りし、配置判定の情報を増やす。
        """
        trial_dig_cnt = 0
        cur_y,cur_x = -1,-1
        while trial_dig_cnt < TRIAL_DIG_NUM and not (self.judge_if_turn_over() or self.judge_if_digged_all()):
            # TLE対策
            self.current_time = time.time()
            if self.current_time - self.start_time >= TIME_LIMIT:
                return

            # 指定した長さまで試し掘りの候補マスを補充
            while self.high_v_S_pos_hq and len(self.trial_dig_cand_pos_list) < TRIAL_DIG_CAND_NUM:
                if not self.high_v_S_pos_hq:
                    break
                v_S,(y,x) = heappop(self.high_v_S_pos_hq)
                self.trial_dig_cand_pos_list.append((v_S,(y,x)))

            # 最初は先頭マスを掘る
            if (cur_y,cur_x) == (-1,-1):
                if not self.trial_dig_cand_pos_list:
                    break
                _,(cur_y,cur_x) = self.trial_dig_cand_pos_list.pop(0)
            # 以降は遠くのマスを掘る
            else:
                best_y,best_x = -1,-1
                max_dist = -1
                max_idx = -1
                for i,(v_S,(y,x)) in enumerate(self.trial_dig_cand_pos_list):
                    dist = abs(y-cur_y) + abs(x-cur_x)
                    # まだ掘り進められていないうちは全体を満遍なく掘りたい
                    if len(self.judge.digged_oil_pos_set) < self.total_oil_amount * TRIAL_DIG_SWITCH_RATIO2:
                        undigged_cnt = 0
                        # まだ周囲に掘られているマスがない地点を優先的に探す(4マスのポリオミノは最後まで掘られず残りやすいので)
                        for dy,dx in MOVE:
                            ny,nx = y+dy,x+dx
                            if 0<=ny<self.N and 0<=nx<self.N and self.judge.oil_map[ny][nx] == -1:
                                undigged_cnt += 1
                        if undigged_cnt == 4:
                            dist *= DIST_WEIGHT
                    else:
                        # 隣接マスにv(y,x)=1のマスがあるマスを優先(油田とそれ以外の境界を掘りたい)
                        for dy,dx in MOVE:
                            ny,nx = y+dy,x+dx
                            if 0<=ny<self.N and 0<=nx<self.N and self.judge.oil_map[ny][nx] == 1:
                                dist *= DIST_WEIGHT
                                break
                    if dist > max_dist:
                        max_dist = dist
                        max_idx = i
                        best_y,best_x = y,x
                cur_y,cur_x = best_y,best_x
                if not self.trial_dig_cand_pos_list:
                    break
                self.trial_dig_cand_pos_list.pop(max_idx)

            # 既に掘っている場合はスキップ
            if self.judge.oil_map[cur_y][cur_x] != -1:
                continue
            # 油田が存在すると確定している場合はスキップ
            if self.judge.definitive_poly_pos_map[cur_y][cur_x]:
                continue
            self.judge.dig_pos(cur_y,cur_x)
            if self.judge_if_turn_over() or self.judge_if_digged_all():
                break
            trial_dig_cnt += 1
        # 使わなかった分を戻す
        for v_S,(y,x) in self.trial_dig_cand_pos_list:
            heappush(self.high_v_S_pos_hq, (-v_S, (y,x)))
       
    def dig_adjacent_pos(self):
        """全ての油田が見つかるまで、既に掘ったマスの隣接マスを掘る
        """
        # 始点の候補を決める(まだ掘られておらず、近くにv(y,x)>0のマスがあり、未発掘の隣接マスが多い)
        dig_cand_pos_list = []
        for y in range(self.N):
            for x in range(self.N):
                # 発掘済みのマスはスキップ
                if self.judge.oil_map[y][x] >= 0:
                    continue
                adjacent_digged_oil_cnt = 0
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if not (0<=ny<self.N and 0<=nx<self.N):
                        continue
                    if self.judge.oil_map[ny][nx] > 0:
                        adjacent_digged_oil_cnt += 1
                score = -self.judge.oil_forecast_map[y][x] if adjacent_digged_oil_cnt == 0 else -4 / adjacent_digged_oil_cnt
                dig_cand_pos_list.append((score,(y,x)))
        
        # adjacent_digged_cntが正かつ小さい値のものを始点にする
        if not dig_cand_pos_list:
            return
        dig_cand_pos_list.sort()

        # 決まった始点の隣接マスをBFSで探索
        start_pos = []
        y,x = dig_cand_pos_list[0][1]
        heappush(start_pos, (y,x))
        while start_pos:
            y,x = heappop(start_pos)
            # 一度も掘られていないマスならば掘り、そうでない場合は確定済のv(S)を使用
            if self.judge.oil_map[y][x] == -1:
                v_S = self.judge.dig_pos(y,x)
                # 上限ターンに達するか全ての埋蔵石油が発掘できたら終了
                if self.judge_if_turn_over() or self.judge_if_digged_all():
                    return
            else:
                v_S = self.judge.oil_map[y][x]
            if v_S == 0:
                continue

            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if 0<=ny<self.N and 0<=nx<self.N and self.judge.oil_map[ny][nx] == -1:
                    heappush(start_pos, (ny,nx))

    def find_optimal_arrangement(self):
        """現時点で分かっている試し掘り情報と矛盾せず、推定v(S)の合計が最大となるポリオミノの配置を探索する。
           1.v(y,x)が0→ポリオミノを置いてはいけない
           2.v(y,x)が1以上→v(y,x)個ちょうどのポリオミノが置かれていないといけない
        """

        def _judge_if_no_contradict(estimate_poly_pos_map):
            """配置に矛盾が無いか確認
            """
            # 配置に矛盾が無いか(v(y,x)>0のマスに丁度v(y,x)個のミノが使われているか)確認
            for y in range(self.N):
                for x in range(self.N):
                    # まだv(y,x)が確定していないマスはスキップ
                    if self.judge.oil_map[y][x] == -1:
                        continue

                    # ポリオミノの置かれたor置かれていない個数が確定したv(y,x)と矛盾する場合は失敗
                    if len(estimate_poly_pos_map[y][x]) != self.judge.oil_map[y][x]:
                        return False
            return True

        ### メイン処理 ###
        # 現時点で確定している情報を基に、v(y,x)>0マスに置けるポリオミノIDを列挙
        occupied_pos_map = [[[] for _ in range(self.N)] for _ in range(self.N)]
        for base_y in range(self.N):
            for base_x in range(self.N):
                for poly_id in self.judge.possible_poly_pos_map[base_y][base_x]:
                    oil = self.OILS[poly_id]
                    for dy,dx in oil.relative_pos_list:
                        ny,nx = base_y+dy,base_x+dx
                        # v(y,x)>0マスに置けるならIDを追加
                        if self.judge.oil_map[ny][nx] > 0:
                            occupied_pos_map[ny][nx].append(poly_id)

        # 一意に置き場所が確定できるポリオミノを探索
        # TODO: あるポリオミノの配置が確定することで他の配置も連鎖的に確定していく場合がある?バグ取れず
        for base_y in range(self.N):
            for base_x in range(self.N):
                # TODO: 本当は全可能性を試したいけどTLEするようなら制限を設ける
                for poly_id in self.judge.possible_poly_pos_map[base_y][base_x]:
                    oil = self.OILS[poly_id]
                    for dy,dx in oil.relative_pos_list:
                        ny,nx = base_y+dy,base_x+dx
                        # v(y,x)>0マスで置けるポリオミノIDの種類数とv(y,x)が一致していれば確定
                        # 同じ種類のポリオミノIDが複数回置ける場合を除外する必要があることに注意
                        # TODO: 確定した時点で、他のマスからはそのpoly_idは存在できなくなる
                        if self.judge.oil_map[ny][nx] > 0 and self.judge.oil_map[ny][nx] == len(occupied_pos_map[ny][nx]) == len(set(occupied_pos_map[ny][nx])):
                            self.judge.definitive_poly_id.add(poly_id)
                            for dy,dx in oil.relative_pos_list:
                                ny,nx = base_y+dy,base_x+dx
                                self.judge.definitive_poly_pos_map[ny][nx].add(poly_id)
                                self.judge.definitive_oil_pos_set.add((ny,nx))
                            break

        # 配置を確定できたポリオミノがある場合はoccupied_pos_mapから当該poly_idを取り除く
        for y in range(self.N):
            for x in range(self.N):
                for poly_id in self.judge.definitive_poly_id:
                    while poly_id in occupied_pos_map[y][x]:
                        occupied_pos_map[y][x].remove(poly_id)

        # 未確定ポリオミノの推定v(S)及び始点座標を配列に格納
        probable_poly_list = self.calc_probable_poly_arrangement()

        # 一意に確定したポリオミノの配置に加え、確定したとみなせるポリオミノも確定扱いすることで組合せ数を減らす
        current_definitive_poly_pos_map = [[set() for _ in range(self.N)] for _ in range(self.N)]
        current_definitive_poly_id = set()
        current_definitive_poly_id |= self.judge.definitive_poly_id
        current_definitive_pos_list = []
        # まずは実際に確定したポリオミノの情報をコピー
        for y in range(self.N):
            for x in range(self.N):
                if self.judge.definitive_poly_pos_map[y][x]:
                    current_definitive_poly_pos_map[y][x] |= self.judge.definitive_poly_pos_map[y][x]
                    current_definitive_pos_list.append((y,x))
        
        # 参考情報(配置の組合せが何通りあるか)
        pattern_num = 1
        for poly_id in range(self.M):
            if poly_id in current_definitive_poly_id:
                continue
            pattern_num *= len(probable_poly_list[poly_id])

        # 組合せが多すぎる場合は探索しない
        if pattern_num >= DFS_LIMIT:
            return set()

        # 確定済及び確定とみなしたポリオミノの配置を基に、未確定ポリオミノの最適配置をDFSで全探索
        best_poly_pos_list = [] # 矛盾なく配置できたポリオミノの座標組合せを降順ソートしたリスト
        current_undefinitive_poly_id = list(set([i for i in range(self.M)]) - current_definitive_poly_id)
        def search_best_poly_pos_dfs(i, total_v_S, current_definitive_poly_pos_map):
            # TLE対策
            self.current_time = time.time()
            if self.current_time - self.start_time >= TIME_LIMIT:
                return
            
            # 最後まで矛盾なく配置できたらtotal_v_Sと配置を記録
            if i == len(current_undefinitive_poly_id):
                if _judge_if_no_contradict(current_definitive_poly_pos_map):
                    final_pos_set = set(current_definitive_pos_list)
                    for y in range(self.N):
                        for x in range(self.N):
                            if current_definitive_poly_pos_map[y][x]:
                                final_pos_set.add((y,x))
                        best_poly_pos_list.append((total_v_S,final_pos_set))
                return

            # probable_poly_listの上位から順に組合せを試す
            poly_id = current_undefinitive_poly_id[i]
            oil = self.OILS[poly_id]
            for estimated_v_S,(base_y,base_x) in probable_poly_list[poly_id][:min(30,len(probable_poly_list[poly_id]))]:
                # TLE対策
                self.current_time = time.time()
                if self.current_time - self.start_time >= TIME_LIMIT:
                    return
                pos_list = []
                failure_flg = False
                for dy,dx in oil.relative_pos_list:
                    ny,nx = base_y+dy,base_x+dx
                    # 仮にポリオミノを置いた(+1)場合に、確定済v(y,x)の値を超える場合は矛盾
                    if self.judge.oil_map[ny][nx] != -1 and len(current_definitive_poly_pos_map[ny][nx]) + 1 > self.judge.oil_map[ny][nx]:
                        failure_flg = True
                        break
                    pos_list.append((ny,nx))
                if failure_flg:
                    continue
                # 問題なければcurrent_definitive_poly_pos_mapにpoly_idを追加して次のpoly_idの探索へ
                for y,x in pos_list:
                    current_definitive_poly_pos_map[y][x].add(poly_id)
                search_best_poly_pos_dfs(i+1, total_v_S+estimated_v_S, current_definitive_poly_pos_map)
                # 後処理
                for y,x in pos_list:
                    current_definitive_poly_pos_map[y][x].remove(poly_id)
                    
        
        search_best_poly_pos_dfs(0, 0, current_definitive_poly_pos_map)
        best_poly_pos_list.sort(reverse=True)

        # 回答用の座標セットを作成
        if best_poly_pos_list:
            poly_pos_set = best_poly_pos_list[0][1]
            if poly_pos_set:
                return poly_pos_set
        return set()

    def calc_probable_poly_arrangement(self):
        """未確定ポリオミノの推定v(S)及び始点座標をv(S)の降順ソート済み配列に格納
        """
        probable_poly_list = [[] for _ in range(self.M)]
        for base_y in range(self.N):
            for base_x in range(self.N):
                for poly_id in self.judge.possible_poly_pos_map[base_y][base_x]:
                    oil = self.OILS[poly_id]
                    estimated_v_S = 0
                    oil_pos_cnt = 0
                    failure_flg = False
                    for dy,dx in oil.relative_pos_list:
                        ny,nx = base_y+dy,base_x+dx
                        if not (0<=ny<self.N and 0<=nx<self.N):
                            failure_flg = True
                            break
                        # ポリオミノを置くべき場所の埋蔵量が0の場合矛盾
                        if self.judge.oil_map[ny][nx] == 0:
                            failure_flg = True
                            break
                        if self.judge.oil_map[ny][nx] > 0:
                            oil_pos_cnt += 1
                        estimated_v_S += self.judge.oil_forecast_map[ny][nx]
                    if failure_flg:
                        continue
                    # TODO: 推定v(S)が小さいポリオミノ配置はスキップする枝刈り。消した方がいいかも
                    if estimated_v_S < oil.n/4:
                        continue
                    probable_poly_list[poly_id].append((estimated_v_S, (base_y,base_x)))

        for i,oil in enumerate(self.OILS):
            probable_poly_list[i].sort(reverse=True)
        
        return probable_poly_list

    def calc_oil_relative_pos(self):
        """各油田(ポリオミノ)の1マス目を基準にした時の残りのマスの相対座標を計算する。
        """
        for i,oil in enumerate(self.OILS):
            relative_pos_list = []
            base_y,base_x = oil.pos_list[0]
            for y,x in oil.pos_list:
                rel_y,rel_x = y-base_y, x-base_x
                relative_pos_list.append((rel_y,rel_x))
        
            self.OILS[i].relative_pos_list = relative_pos_list

    def interpolate_unforecast_v_S(self):
        """未占いマス(値が-1.0)の値を隣接マスの平均で補間する。
        """
        while 1:
            cnt_unforecast_pos = 0
            for y in range(self.N):
                for x in range(self.N):
                    if self.judge.oil_forecast_map[y][x] == -1.0:
                        interpolate_v_S = 0
                        cnt = 0
                        for dy,dx in MOVE:
                            ny,nx = y+dy,x+dx
                            if 0<=ny<self.N and 0<=nx<self.N and self.judge.oil_forecast_map[ny][nx] != -1.0:
                                interpolate_v_S += self.judge.oil_forecast_map[ny][nx]
                                cnt += 1
                        if cnt > 0:
                            self.judge.oil_forecast_map[y][x] = interpolate_v_S / cnt
                        else:
                            cnt_unforecast_pos += 1

            if cnt_unforecast_pos == 0:
                return

    def create_sorted_pos_list(self):
        """試し掘りの候補座標選定のため、占い結果の全座標をスコアが高い順になるように管理する。
        """
        for y in range(self.N):
            for x in range(self.N):
                v_S = self.judge.oil_forecast_map[y][x]
                heappush(self.high_v_S_pos_hq, (-v_S,(y,x)))

    def judge_if_turn_over(self):
        """全ターンを使い切ったか判定する
        """
        return self.judge.turn == self.judge.turn_limit
    
    def judge_if_digged_all(self):
        """全ての油田が見つかったか判定する
        """
        if self.judge.digged_oil_amount == self.total_oil_amount or len(self.judge.digged_total_pos_set | self.judge.definitive_oil_pos_set) == self.N**2:
            return True
        return False
    

def main():
    N,M,EPS = map(str, input().split())
    N = int(N)
    M = int(M)
    EPS = float(EPS)

    OILS = []
    for _ in range(M):
        n,*yx = list(map(int,input().split()))
        pos_list = []
        for i in range(len(yx)//2):
            pos_list.append((yx[2*i],yx[2*i+1]))
        OILS.append(OIL(n,pos_list,[]))

    solver = Solver(N,M,EPS,OILS)
    solver.solve()

if __name__ == "__main__":
    main()
