from dataclasses import dataclass
from typing import List
from collections import defaultdict
from heapq import heappush, heappop
import sys
input = lambda: sys.stdin.readline().rstrip()

### CONST ###
INF = 10**18
FORECAST_LEN = 3 # 占う正方形領域の一辺の長さ
MIN_v_S_DIG = 2 # 占った領域内を掘るかどうかの閾値(この値以上なら掘る)
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])
MOVE_AROUND = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動

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
    def __init__(self, n: int, m: int, eps: float):
        self.N = n
        self.M = m
        self.EPS = eps

        self.turn = 0
        self.turn_limit = 2 * n**2
        self.cost = 0
        self.digged_oil_pos_set = set()
        self.digged_oil_amount = 0 # これまでに発掘された総油田量

        # フィールド管理用変数
        self.oil_map = [[-1]*n for _ in range(n)] # 確定した油田の埋蔵量の地図(-1:不明、0以上：確定)
        self.forecast_group_len = -(-(n)//FORECAST_LEN) # 島の一辺が何個のグループに分割できるか
        self.oil_forecast_map = [[-1]*self.forecast_group_len for _ in range(self.forecast_group_len)] # FORECAST_LEN**2の正方形領域ごとに占った埋蔵量
        self.oil_forecast_gridmap = [[0.0]*n for _ in range(n)] # マスごとの予想埋蔵量


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
        return actual_oil_amount

    def forecast_pos_list(self, pos_list: list[list[int]], gr_y: int = -1, gr_x: int = -1) -> int:
        """指定したマスの集合が持つ石油埋蔵量を占う

        Args:
            pos (list[list[int]): 占う対象のマスのリスト
        """
        if self.turn == self.turn_limit:
            return

        assert len(pos_list) > 1 # 占うマスは2マス以上必要

        req = ["q"]
        req.append(len(pos_list))
        for y,x in pos_list:
            req.append(y)
            req.append(x)
        
        print(*req, flush=True)

        self.turn += 1
        self.cost += 1 / (len(pos_list))**0.5
        forecasted_oil_amount = int(input())
        # FORECAST_LEN*FORECAST_LENの正方形領域で走査した時はself.oil_forecast_mapを更新
        if [gr_y, gr_x] != [-1,-1]:
            self.oil_forecast_map[gr_y][gr_x] = forecasted_oil_amount

        # 占った座標リストにv(S)を分配
        for y,x in pos_list:
            self.oil_forecast_gridmap[y][x] += forecasted_oil_amount / len(pos_list)

        return forecasted_oil_amount
    
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
        self.judge = Judge(n,m,eps)

        self.cost = 0
        self.score = 0
        self.total_oil_amount = sum([oil.n for oil in oils]) # 埋蔵されている全油田量

        # FORECAST_LEN(占い領域)、v(S)ごとに平均μの値を事前計算
        self.norm_means = defaultdict(int) # (forecast_len, v(S))がキー、正規分布の平均μがバリュー
        self.calc_norm_means()

    def solve(self) -> int:

        # 3x3マスを走査して予想埋蔵量のグリッドマップを作るテスト
        for y in range(self.N-FORECAST_LEN+1):
            for x in range(self.N-FORECAST_LEN+1):
                pos_list = []
                for dy in range(FORECAST_LEN):
                    for dx in range(FORECAST_LEN):
                        ny,nx = y+dy,x+dx
                        if not (0<=ny<self.N and 0<=nx<self.N):
                            continue
                        pos_list.append((ny,nx))
                if len(pos_list) > 1:
                    self.judge.forecast_pos_list(pos_list)
        
        print(*self.judge.oil_forecast_gridmap, sep="\n", file=sys.stderr)

        # ここから2個目の方針解(M=2,3の時限定)
        # 1.ポリオミノの形そのままにスライドさせて最もv(S)が大きくなったところを解とする
        if self.M == 2:
            oil_pos_set = self.slide_optimal_oil_pos()
            if oil_pos_set:
                finish_flg = self.judge.answer(oil_pos_set)
                if finish_flg:
                    return

        # ここから初期方針解
        # 1. N*Nの島全体をFORECAST_LEN*FORECAST_LENのグループに区切ってそれぞれの埋蔵量を占う
        self.forecast_all_group()
        if self.judge.turn == self.judge.turn_limit:
            return
        self.judge.debug()

        # 2. 試し掘りと隣接マス発掘を繰り返す
        while 1:
            # 上限ターンに達するか全ての埋蔵石油が発掘できたら終了
            if self.judge.turn == self.judge.turn_limit or self.judge_if_digged_all():
                break

            # 隣接マス発掘の始点候補(heapqで(-v_S,y,x)として管理)
            self.start_pos = []

            # 2-1. 油田がある可能性があるグループ内の1マスを試し掘り。見つかったら隣接マス発掘の始点候補に追加
            self.dig_probable_group()
            # 上限ターンに達するか全ての埋蔵石油が発掘できたら終了
            if self.judge.turn == self.judge.turn_limit or self.judge_if_digged_all():
                break
            # self.judge.debug()

            # 2-2. 全ての油田が見つかるまで、発掘済みの油田マスの隣接マスを掘る
            if not self.judge_if_digged_all():
                self.dig_adjacent_pos()
        
        # 4. 全ての油田が発掘できたら答えを出力する
        self.judge.answer(self.judge.digged_oil_pos_set)

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
        
        def _forecast_and_update(i,oil,forecast_pos_list,max_v_S,best_oil_pos_list):
            """当該油田ポリオミノの全マスが島の範囲内に存在する場合、占いを実行し最適油田位置を更新する。
            """
            v_S = -1
            if len(forecast_pos_list) != oil.n:
                return v_S
            v_S = self.judge.forecast_pos_list(forecast_pos_list)
            # 上限ターンに達したら終了
            if self.judge.turn == self.judge.turn_limit:
                return
            if v_S > max_v_S[i]:
                max_v_S[i] = v_S
                best_oil_pos_list[i] = forecast_pos_list
            return v_S

        # メイン処理
        max_v_S = [0]*self.M
        best_oil_pos_list = [[] for _ in range(self.M)]
        oil_pos_set = set() # 回答用の座標セット格納変数

        # 最初にFORECAST_LENだけ間隔を空けて占い、付近に油田がありそうなマスだけ再占いのために保存する
        research_pos_list = [[] for _ in range(self.M)]
        for i,oil in enumerate(self.OILS):
            for gr_y in range(self.N//FORECAST_LEN):
                for gr_x in range(self.N//FORECAST_LEN):
                    base_y,base_x = gr_y*FORECAST_LEN+oil.pos_list[0][0], gr_x*FORECAST_LEN+oil.pos_list[0][1]
                    forecast_pos_list = _calc_forecast_pos_list(base_y,base_x,oil)
                    # 上限ターンに達したら終了
                    if self.judge.turn == self.judge.turn_limit:
                        return
                    v_S = _forecast_and_update(i,oil,forecast_pos_list,max_v_S,best_oil_pos_list)
                    # v(S)が大きいマスは付近に油田がある可能性が高いため再占いのために保存
                    if v_S > oil.n // 4:
                        research_pos_list[i].append((base_y,base_x))

        # 付近に油田がある可能性が高いマス周辺を再占い
        for i,oil in enumerate(self.OILS):
            for base_y,base_x in research_pos_list[i]:
                for dy,dx in MOVE_AROUND:
                    ny,nx = base_y+dy, base_x+dx
                    forecast_pos_list = _calc_forecast_pos_list(ny,nx,oil)
                    _forecast_and_update(i,oil,forecast_pos_list,max_v_S,best_oil_pos_list)
                    # 上限ターンに達したら終了
                    if self.judge.turn == self.judge.turn_limit:
                        return oil_pos_set
                    
        # スライドして見つけた油田の位置を回答
        for oil_pos_list in best_oil_pos_list:
            oil_pos_set |= set(oil_pos_list)

        return oil_pos_set

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

    def calc_norm_means(self):
        """FORECAST_LEN(占い領域)、v(S)ごとに平均μの値を計算する
        """
        for forecast_len in range(1,self.N+1):
            for v_S in range(self.M * forecast_len**2 + 1):
                # FORECAST_LEN**2の正方形領域に対してv(S)=0になる正規分布関数の平均値μを格納
                self.norm_means[(forecast_len,v_S)] = (forecast_len - v_S) * self.EPS + v_S * (1 - self.EPS)

    def forecast_all_group(self) -> None:
        """N*Nの島全体をFORECAST_LEN*FORECAST_LENの座標グループに区切ってそれぞれの埋蔵量を占う
        """
        #TODO: 油田出現頻度の高いグループから順に占っていく(例：中央から外に向けて)とか、油田発見次第その回の処理を打ち切るとか
        for gr_y in range(self.judge.forecast_group_len):
            for gr_x in range(self.judge.forecast_group_len):
                pos_list = []
                for dy in range(FORECAST_LEN):
                    for dx in range(FORECAST_LEN):
                        y,x = FORECAST_LEN * gr_y + dy, FORECAST_LEN * gr_x + dx
                        if not (0<=y<self.N and 0<=x<self.N):
                            continue
                        pos_list.append((y,x))
                if len(pos_list) > 1:
                    self.judge.forecast_pos_list(pos_list, gr_y, gr_x)
                    # 上限ターンに達したら終了
                    if self.judge.turn == self.judge.turn_limit:
                        return

    def judge_if_dig(self, gr_y, gr_x):
        """占った領域に含まれるマスを掘るべきか(=埋蔵量0でないか)を判定
        """
        # 当該領域が占われていなかったら掘らない
        if self.judge.oil_forecast_map[gr_y][gr_x] == -1:
            return False

        estimated_oil_amount = -1
        min_diff = INF
        for v_S in range(self.M * FORECAST_LEN**2 + 1):
            diff = abs(self.judge.oil_forecast_map[gr_y][gr_x] - self.norm_means[(FORECAST_LEN, v_S)])
            if diff < min_diff:
                min_diff = diff
                estimated_oil_amount = v_S
        
        # 予想v(S)>MIN_v_S_DIGの場合は掘るべきと判断
        if estimated_oil_amount >= MIN_v_S_DIG:
            return True
        
        return False

    def dig_probable_group(self) -> None:
        """油田がある可能性があるグループ内の1マスを試し掘り。
           見つかったら隣接マス発掘の始点候補に追加。
        """
        for gr_y in range(self.judge.forecast_group_len):
            for gr_x in range(self.judge.forecast_group_len):
                # 占いの結果を基に掘るべきグループ(油田がありそう)か判断
                if not self.judge_if_dig(gr_y, gr_x):
                    continue
                
                # グループ内のマスを1つずつ掘る
                # TODO: 掘っていくうちに絶対にこのポリオミノだと確定して手数を減らせないか検討
                group_finish_flag = False
                for dy in range(FORECAST_LEN):
                    for dx in range(FORECAST_LEN):                        
                        y,x = FORECAST_LEN * gr_y + dy, FORECAST_LEN * gr_x + dx
                        if 0<=y<self.N and 0<=x<self.N and self.judge.oil_map[y][x] == -1:
                            # まだ掘っていない1マスを掘ってそのグループは終了。石油埋蔵マスなら隣接マス発掘始点候補に追加。
                            v_S = self.judge.dig_pos(y,x)
                            # 上限ターンに達するか全ての埋蔵石油が発掘できたら終了
                            if self.judge.turn == self.judge.turn_limit or self.judge_if_digged_all():
                                return

                            if v_S > 0:
                                heappush(self.start_pos, (-v_S,y,x))
                            group_finish_flag = True
                            break
                    if group_finish_flag:
                        break
                    
    def dig_adjacent_pos(self):
        """全ての油田が見つかるまで、既に掘ったマス(油田マス優先)の隣接マスを掘る
        """
        #TODO: 掘るべきマスを賢く決められないか検討(例：隣接マスでなく、ポリオミノの特定に必要なマスを決め打ち)
        while self.start_pos:
            # self.calc_polyomino_uniqueness()

            _,y,x = heappop(self.start_pos)
            # 一度も掘られていないマスならば掘り、そうでない場合は確定済のv(S)を使用
            if self.judge.oil_map[y][x] == -1:
                v_S = self.judge.dig_pos(y,x)
                # 上限ターンに達するか全ての埋蔵石油が発掘できたら終了
                if self.judge.turn == self.judge.turn_limit or self.judge_if_digged_all():
                    return
            else:
                v_S = self.judge.oil_map[y][x]
            if v_S == 0:
                continue

            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if 0<=ny<self.N and 0<=nx<self.N and self.judge.oil_map[ny][nx] == -1:
                    heappush(self.start_pos, (-v_S,ny,nx))

    # def calc_polyomino_uniqueness(self):
    #     """現在分かっている油田埋蔵量の情報を元に各ポリオミノの位置を一意に決定できるか計算する。
    #        全ての油田の位置が一意に決定できたらその時点で回答する。
    #     """

    #     # 現時点の情報で矛盾なく各油田を置ける場所にフラグを立てる
    #     occupied_pos = [[False]*self.N for _ in range(self.N)]

    #     #TODO: self.OILSをoil.nの大きい順にソートしておき、前から順番に座標確定させていく

    #     for i,oil in enumerate(self.OILS):
    #         for y in range(self.N):
    #             for x in range(self.N):
    #                 base_y,base_x = y+oil.pos_list[0][0],x+oil.pos_list[0][1]
    #                 for dy,dx in oil.relative_pos_list:
    #                     ny,nx = base_y+dy,base_x+dx
    #                     if not (0<=ny<self.N and 0<=nx<self.N):
    #                         continue
    #                     # 当該座標の油田量が確定している、かつ油田が存在しない(v(S)=0)場合はスキップ
    #                     if self.judge.oil_map[ny][nx] == 0:
    #                         continue
                    
    #                 # 矛盾なく置けた場合は座標(occupied_pos)を確定

    #     # 全ての油田が矛盾なく一意に特定可能な場所に置けた場合、その時点で解を出力

    def judge_if_digged_all(self):
        """全ての油田が見つかったか判定する
        """
        # 全ての埋蔵石油が発掘できたら終了
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
