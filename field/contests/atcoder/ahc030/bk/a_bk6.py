from dataclasses import dataclass
from typing import List
from heapq import heappush, heappop
import random
import sys
input = lambda: sys.stdin.readline().rstrip()

### CONST ###
INF = 10**18
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
MOVE_AROUND = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動

FORECAST_INTERVAL = 2 # ポリオミノの形そのままで占う時の間隔
RESEARCH_TOP_K = 5 # ポリオミノの形そのままで占った結果、v(S)上位何個に対し隣接マスを再調査するか
FORECAST_LEN = 3 # 占う正方形領域の一辺の長さ
TRIAL_DIG_NUM = 10 # 1ターンで何回試し掘りするか
TRIAL_DIG_CAND_NUM = 3 # 毎回の試し掘り場所決めの候補とする座標の数

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
        self.digged_oil_pos_set = set() # これまでに発掘した場所
        self.digged_oil_amount = 0 # これまでに発掘された総油田量
        self.definitive_pos_set = set() # 発掘していないが油田があると確定した場所

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
            return

        req = ["q", 1, y, x]
        print(*req, flush=True)

        self.turn += 1
        self.cost += 1
        actual_oil_amount = int(input())

        # v(S)>0なら油田の座標セットに追加
        if actual_oil_amount > 0:
            self.digged_oil_pos_set.add((y,x))

            # (y,x)の発掘が初めてかつv(S)>0なら発掘済み油田量に加算
            if self.oil_map[y][x] != actual_oil_amount:
                self.digged_oil_amount += actual_oil_amount

        self.oil_map[y][x] = actual_oil_amount
        self.update_possible_poly_map()
        # print(self.turn, file=sys.stderr)
        # print(*self.possible_poly_map, sep="\n",file=sys.stderr)
        # print(file=sys.stderr)
        return actual_oil_amount

    def initialize_possible_poly_map(self) -> int:
        """初期状態で各ポリオミノが存在できるマスの情報を管理
        """
        for i,oil in enumerate(self.OILS):
            for base_y in range(self.N):
                for base_x in range(self.N):
                    poly_pos = []
                    failure_flg = False
                    for dy,dx in oil.relative_pos_list:
                        ny,nx = base_y+dy,base_x+dx
                        if not (0<=ny<self.N and 0<=nx<self.N):
                            failure_flg = True
                            break
                        poly_pos.append((ny,nx))
                    if failure_flg:
                        continue
                    for y,x in poly_pos:
                        self.possible_poly_pos_map[y][x].add(i)

    def update_possible_poly_map(self) -> int:
        """掘る度に各ポリオミノが存在できるマスの情報を更新
        """
        for i,oil in enumerate(self.OILS):
            for base_y in range(self.N):
                for base_x in range(self.N):
                    poly_pos = []
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
                        # 配置が確定したポリオミノがある地点にも置けない
                        if self.oil_map[ny][nx] > 0 and len(self.definitive_poly_pos_map[ny][nx]) == self.oil_map[ny][nx] and i not in self.definitive_poly_pos_map[ny][nx]:
                            failure_flg = True
                            break
                        poly_pos.append((ny,nx))

                    if failure_flg:
                        if i in self.possible_poly_pos_map[base_y][base_x]:
                            self.possible_poly_pos_map[base_y][base_x].remove(i)
                        continue

    def forecast_pos_list(self, pos_list: list[list[int]]) -> int:
        """指定したマスの集合が持つ石油埋蔵量を占う

        Args:
            pos (list[list[int]): 占う対象のマスのリスト
        """
        if self.turn == self.turn_limit:
            return

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
    
    def answer(self, pos_set: set) -> None:
        """見つかった全ての油田の座標を出力
        """
        if self.turn == self.turn_limit:
            return

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
        
        # ここから2個目の方針解(M=2の時限定)
        # 1.ポリオミノの形そのままにスライドさせて最もv(S)が大きくなったところを解とする
        if self.M <= 0:
            oil_pos_set = self.slide_optimal_oil_pos()
            if oil_pos_set:
                finish_flg = self.judge.answer(oil_pos_set)
                if finish_flg:
                    return

        self.judge.debug()

        # ここから初期方針解
        # 1. N*Nの島全体をFORECAST_LEN*FORECAST_LENのグループに区切ってそれぞれの埋蔵量を占う
        self.forecast_all_group()
        # print(*self.judge.oil_forecast_map, sep="\n", file=sys.stderr)
        if self.judge_if_turn_over():
            return
        self.judge.debug()

        # 2. 試し掘りと隣接マス発掘を繰り返す
        while 1:
            # 上限ターンに達するか全ての埋蔵石油が発掘できたら終了
            if self.judge_if_turn_over() or self.judge_if_digged_all():
                break

            self.trial_dig()

            # 2-1. 油田がある可能性があるグループ内の1マスを試し掘り。見つかったら隣接マス発掘の始点候補に追加
            # v_S,y,x = self.dig_probable_pos()
            # 上限ターンに達するか全ての埋蔵石油が発掘できたら終了
            if self.judge_if_turn_over() or self.judge_if_digged_all():
                break
            # self.judge.debug()

            # 2-2. 全ての油田が見つかるまで、発掘済みの油田マスの隣接マスを掘る
            # if not self.judge_if_digged_all():
            #     self.dig_adjacent_pos(v_S,y,x)

            # 3. 現時点の情報を基に、最適な配置を探索する
            oil_pos_set = self.find_optimal_arrangement()

            # 3-3. その時点での最適な配置予想を回答する。
            if oil_pos_set:
                finish_flg = self.judge.answer(oil_pos_set)
                if finish_flg:
                    return

        # 4. 全ての油田が発掘できたら答えを出力する
        self.judge.answer(self.judge.digged_oil_pos_set | self.judge.definitive_pos_set)

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
                    return forecast_pos_list
                forecast_pos_list.append((ny,nx))
            return forecast_pos_list

        def _judge_if_skip(forecast_pos_list):
            """これまでの占い結果をもとに今回占うポリオミノの領域の推定v(S)が小さそうならスキップする。
            """
            estimated_v_S = 0
            cnt_not_updated = 0 # 初期値(-1.0)のまま更新されていないマスの数
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
            for j in range(RESEARCH_TOP_K):
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

    def forecast_all_group(self) -> None:
        """N*Nの島全体をFORECAST_LEN*FORECAST_LENの座標グループに区切ってそれぞれの埋蔵量を占う
        """
        #TODO: 油田出現頻度の高いグループから順に占っていく(例：中央から外に向けて)とか、油田発見次第その回の処理を打ち切るとか
        forecast_group_len = -(-(self.N)//FORECAST_LEN) # 島の一辺(N)をFORECASTで割った時のceil
        # より正確なv(S)が測れるように1マスずつ縦横をずらして2回測定
        for diff in range(2):
            for gr_y in range(forecast_group_len):
                for gr_x in range(forecast_group_len):
                    pos_list = []
                    for dy in range(FORECAST_LEN):
                        for dx in range(FORECAST_LEN):
                            y,x = FORECAST_LEN * gr_y + dy + diff, FORECAST_LEN * gr_x + dx + diff
                            if not (0<=y<self.N and 0<=x<self.N):
                                continue
                            pos_list.append((y,x))
                    if len(pos_list) > 1:
                        self.judge.forecast_pos_list(pos_list)
                        # 上限ターンに達したら終了
                        if self.judge_if_turn_over():
                            return
        
        # 占い結果の推定v(S)が高い順になるよう座標を管理
        for y in range(self.N):
            for x in range(self.N):
                v_S = self.judge.oil_forecast_map[y][x]
                if v_S != -1.0:
                    heappush(self.high_v_S_pos_hq, (-v_S,(y,x)))

    def trial_dig(self) -> None:
        """油田が見つかる可能性が高いマスをいくつか試し掘りし、配置判定の情報を増やす。
        """
        trial_dig_cnt = 0
        cur_y,cur_x = -1,-1
        while trial_dig_cnt < TRIAL_DIG_NUM and not (self.judge_if_turn_over() or self.judge_if_digged_all()):
            # 指定した長さまで試し掘りの候補マスを補充
            while self.high_v_S_pos_hq and len(self.trial_dig_cand_pos_list) < TRIAL_DIG_CAND_NUM:
                v_S,(y,x) = heappop(self.high_v_S_pos_hq)
                self.trial_dig_cand_pos_list.append((v_S,(y,x)))

            # 最初は先頭マスを掘る
            if (cur_y,cur_x) == (-1,-1):
                if not self.trial_dig_cand_pos_list:
                    return
                _,(cur_y,cur_x) = self.trial_dig_cand_pos_list.pop(0)
            # 以降は遠くのマスを掘る
            else:
                best_y,best_x = -1,-1
                max_dist = -1
                max_idx = -1
                for i,(v_S,(y,x)) in enumerate(self.trial_dig_cand_pos_list):
                    dist = abs(y-cur_y) + abs(x-cur_x)
                    if dist > max_dist:
                        max_dist = dist
                        max_idx = i
                        best_y,best_x = y,x
                cur_y,cur_x = best_y,best_x
                if not self.trial_dig_cand_pos_list:
                    return
                self.trial_dig_cand_pos_list.pop(max_idx)

            # 既に掘っている場はスキップ
            if self.judge.oil_map[cur_y][cur_x] != -1:
                continue
            # 油田が存在すると確定している場合はスキップ
            if (cur_y,cur_x) in self.judge.definitive_pos_set:
                continue
            self.judge.dig_pos(cur_y,cur_x)
            trial_dig_cnt += 1

    def find_optimal_arrangement(self):
        """現時点で分かっている試し掘り情報と矛盾せず、推定v(S)の合計が最大となるポリオミノの配置を探索する。
           1.v(y,x)が0→ポリオミノを置いてはいけない
           2.v(y,x)が1以上→v(y,x)個ちょうどのポリオミノが置かれていないといけない
        """

        def _judge_if_no_contradict(estimate_oil_map):
            """配置に矛盾が無いか確認
            """
            # 配置に矛盾が無いか(v(y,x)>0のマスに丁度v(y,x)個のミノが使われているか)確認
            for y in range(self.N):
                for x in range(self.N):
                    # まだv(y,x)が確定していないマスはスキップ
                    if self.judge.oil_map[y][x] == -1:
                        continue

                    # ポリオミノの置かれたor置かれていない個数が確定したv(y,x)と矛盾する場合は失敗
                    if len(estimate_oil_map[y][x]) != self.judge.oil_map[y][x]:
                        return False
            return True

        def _randomize_initial_pos_list():
            """現時点で分かっている試し掘り情報と矛盾せず、推定v(S)の合計が最大となるポリオミノの初期配置をランダムに決定
            """
            # TODO: 初期配置の探索を何回ループさせるかパラメータ調整要
            
            for _ in range(1000):
                base_pos_list = [[-1,-1] for _ in range(self.M)]
                estimate_oil_map = [[[] for _ in range(self.N)] for _ in range(self.N)]
                failure_flg = False
                for i,oil in enumerate(self.OILS):
                    rand = random.randint(0,len(self.best_poly_pos_list[i])-1)
                    _,(base_y,base_x) = self.best_poly_pos_list[i][rand]
                    for dy,dx in oil.relative_pos_list:
                        ny,nx = base_y+dy,base_x+dx
                        # 既に他のポリオミノが置かれていてもう置けない場合
                        if len(estimate_oil_map[ny][nx]) == self.judge.oil_map[ny][nx]:
                            failure_flg = True
                            break
                        base_pos_list[i] = [base_y,base_x]
                        estimate_oil_map[ny][nx].append(i)

                if failure_flg:
                    continue

                if _judge_if_no_contradict(estimate_oil_map):
                    return base_pos_list, estimate_oil_map

            # 矛盾の無い配置が見つからなかった場合は空配列を返す
            return [], []


        ### メイン処理 ###
        # 現時点で確定している情報を基に、v(y,x)>0マスに置けるポリオミノIDを列挙
        occupied_pos_map = [[[] for _ in range(self.N)] for _ in range(self.N)]
        for base_y in range(self.N):
            for base_x in range(self.N):
                # TODO: 本当は全可能性を試したいけどTLEするようなら制限を設ける
                # if len(self.judge.possible_poly_map[base_y][base_x]) > 5:
                #     continue
                for poly_id in self.judge.possible_poly_pos_map[base_y][base_x]:
                    oil = self.OILS[poly_id]
                    for dy,dx in oil.relative_pos_list:
                        ny,nx = base_y+dy,base_x+dx
                        # v(y,x)>0マスに置けるならIDを追加
                        if self.judge.oil_map[ny][nx] > 0:
                            occupied_pos_map[ny][nx].append(poly_id)

        # 一意に置き場所が確定できるポリオミノを探索
        # あるポリオミノの配置が確定することで他の配置も連鎖的に確定していく場合があるため変化がなくなるまでループ
        defined_poly_id = set()
        cnt_defined = 0
        while cnt_defined == 0:
            for base_y in range(self.N):
                for base_x in range(self.N):
                    # TODO: 本当は全可能性を試したいけどTLEするようなら制限を設ける
                    defined_flg = False
                    for poly_id in self.judge.possible_poly_pos_map[base_y][base_x]:
                        oil = self.OILS[poly_id]
                        for dy,dx in oil.relative_pos_list:
                            ny,nx = base_y+dy,base_x+dx
                            # v(y,x)>0マスで置けるポリオミノIDの種類数とv(y,x)が一致していれば確定
                            # 同じ種類のポリオミノIDが複数回置ける場合を除外する必要があることに注意
                            # TODO: 確定した時点で、他のマスからはそのpoly_idは存在できなくなる
                            if self.judge.oil_map[ny][nx] > 0 and self.judge.oil_map[ny][nx] == len(occupied_pos_map[ny][nx]) == len(set(occupied_pos_map[ny][nx])):
                                cnt_defined += 1
                                defined_poly_id.add(poly_id)
                                defined_flg = True
                                break
                        # ポリオミノの配置が確定した場合
                        if defined_flg:
                            for dy,dx in oil.relative_pos_list:
                                ny,nx = base_y+dy,base_x+dx
                                self.judge.definitive_poly_pos_map[ny][nx].add(poly_id)
                                self.judge.definitive_pos_set.add((ny,nx))
                            break

            if cnt_defined == 0:
                break
            # 配置を確定できたポリオミノがある場合はoccupied_pos_mapから当該poly_idを取り除く
            for y in range(self.N):
                for x in range(self.N):
                    for poly_id in defined_poly_id:
                        while poly_id in occupied_pos_map[y][x]:
                            occupied_pos_map[y][x].remove(poly_id)

        # print(self.judge.turn, file=sys.stderr)
        # print(*self.judge.possible_poly_pos_map, sep="\n",file=sys.stderr)
        # print(file=sys.stderr)

        print(self.judge.turn, file=sys.stderr)
        print(*occupied_pos_map, sep="\n",file=sys.stderr)
        print(file=sys.stderr)
        
        print(self.judge.turn, file=sys.stderr)
        print(*self.judge.definitive_poly_pos_map, sep="\n",file=sys.stderr)
        print(file=sys.stderr)

        # 各ポリオミノの推定v(S)及び始点座標を配列に格納
        # if not self.probable_poly_list[0]:
        #     self.calc_probable_poly_arrangement()
        

        # 矛盾を起こさない初期配置を数パターン試す
        # for _ in range(5):
        #     base_pos_list, estimate_oil_map = _randomize_initial_pos_list()
        #     if base_pos_list == [] and estimate_oil_map == []:
        #         continue

        # 回答用の座標セットを作成
        oil_pos_set = set()
        found_poly_ids = set()
        for y in range(self.N):
            for x in range(self.N):
                if len(self.judge.definitive_poly_pos_map[y][x]) > 0:
                    oil_pos_set.add((y,x))
                    found_poly_ids |= self.judge.definitive_poly_pos_map[y][x]
        # if oil_pos_set and len(found_poly_ids) == self.M:
        if oil_pos_set:
            return oil_pos_set
        else:
            return set()

    def calc_oil_relative_pos(self):
        """各油田(ポリオミノ)の1マス目を基準にした時の残りのマスの相対座標を計算する。
        """
        for i,oil in enumerate(self.OILS):
            relative_pos_list = []
            base_y,base_x = oil.pos_list[0]
            relative_pos_list.append((0,0))
            for y,x in oil.pos_list[1:]:
                rel_y,rel_x = y-base_y, x-base_x
                relative_pos_list.append((rel_y,rel_x))
        
            self.OILS[i].relative_pos_list = relative_pos_list

    def judge_if_turn_over(self):
        """全ターンを使い切ったか判定する
        """
        return self.judge.turn == self.judge.turn_limit
    
    def judge_if_digged_all(self):
        """全ての油田が見つかったか判定する
        """
        return self.judge.digged_oil_amount == self.total_oil_amount


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
