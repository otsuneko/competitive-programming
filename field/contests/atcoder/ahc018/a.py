from enum import Enum
from typing import List
import sys
sys.setrecursionlimit(10**7)
import time
import random
from heapq import heappush, heappop
from collections import deque

# 定数
TIME_LIMIT = 4.0
INF = 10**18
DIR = {"U":(-1,0), "R":(0,1), "D":(1,0), "L":(0,-1)}
MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1])

INI_HP = 3000 # 各マスの頑丈さの初期値(仮決め)
INI_WATER_HP = 100 # 水源周辺の頑丈さの初期値(仮決め)
AROUND_DIST = 6 # 岩盤の頑丈さを初期化/更新する際に周辺何マスを処理に含めるか
INVESTIGATE_DIST = 11 # 何マス離れたマスを探索するか(AROUND_DIST < INVESTIGATE_DISTとなる必要あり)
ADDITIONAL_INVESTIGATE_DIST = 11# 何マス離れたマスを追加で探索するか(AROUND_DIST < INVESTIGATE_DISTとなる必要あり)

# Cの値に対する岩盤調査時の力と最大掘削回数、岩盤破壊処理時の力の変換テーブル
MAP_C_INVESTIGATE_POWER = {1:20, 2:20, 4:25, 8:30, 16:50, 32:60, 64:100, 128:200}
MAP_C_INVESTIGATE_LOOP = {1:20, 2:20, 4:16, 8:14, 16:8, 32:7, 64:4, 128:2}
MAP_C_DESTRUCT_POWER = {1:20, 2:20, 4:40, 8:60, 16:80, 32:150, 64:300, 128:500}

# Cの値に対する岩盤追加調査時の力と最大掘削回数の変換テーブル
MAP_C_ADDITIONAL_INVESTIGATE_POWER = {1:10, 2:10, 4:20, 8:30, 16:30, 32:60, 64:60, 128:60}
MAP_C_ADDITIONAL_INVESTIGATE_LOOP = {1:6, 2:6, 4:3, 8:2, 16:2, 32:1, 64:1, 128:1}

# 岩盤の調査結果ステータス(-1:未調査、0：調査済だが水源には繋がらない、1:調査済で水源に繋がる)
class INVESTIGATED_STATUS(Enum):
    NO = -1
    INVESTIGATED = 0
    CONNECT_TO_WATER = 1

SMOOTHING_AREA = 13 # 何マスｘ何マスの平滑化フィルタを作成するか
MASK = [[1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169],
        [1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169,1/169]]

# 座標
class Pos:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

# 出力に対する返り値
class Response(Enum):
    NOT_BROKEN = 0
    BROKEN = 1
    FINISH = 2
    INVALID = -1

# NxNの土地が持つ情報
class Field:

    def __init__(self, N: int, C: int):
        self.C = C
        self.is_broken = [[False] * N for _ in range(N)] # その座標の岩盤が破壊済か
        self.is_investigated = [[INVESTIGATED_STATUS.NO] * N for _ in range(N)] # その座標の頑丈さを調査済か
        self.total_cost = 0
        # フィールドの各マスの頑丈さの推定値を初期化
        self.current_HP = [[INI_HP] * N for _ in range(N)]

    def query(self, y: int, x: int, power: int) -> Response:
        self.total_cost += power + self.C
        print(f"{y} {x} {power}", flush=True)
        res = Response(int(input()))
        if res in (Response.BROKEN, Response.FINISH):
            self.is_broken[y][x] = True
        return res

class Solver:

    def __init__(self, N: int, water_pos: List[Pos], house_pos: List[Pos], C: int):
        self.N = N
        self.water_pos = water_pos
        self.house_pos = house_pos
        self.C = C
        self.field = Field(N, C)
        self.found_water_pos = set()
        self.is_house_connect_to_water = dict()
        self.INVESTIGATE_POWER = MAP_C_INVESTIGATE_POWER[C]
        self.INVESTIGATE_LOOP = MAP_C_INVESTIGATE_LOOP[C]
        self.ADDITIONAL_INVESTIGATE_POWER = MAP_C_ADDITIONAL_INVESTIGATE_POWER[C]
        self.ADDITIONAL_INVESTIGATE_LOOP = MAP_C_ADDITIONAL_INVESTIGATE_LOOP[C]

        # 家の岩盤を破壊し、周囲の頑丈さを与えたダメージで初期化&調査済にする
        for house in self.house_pos:
            self.destruct(house, self.INVESTIGATE_POWER)
            self.update_investigated_area(house, INVESTIGATED_STATUS.INVESTIGATED)

            # 各家から水源に至るルートが調査済かのステータス初期化
            self.is_house_connect_to_water[house] = False

        # 水源の周囲の頑丈さをINI_WATER_HPで初期化
        for water in self.water_pos:
            self.update_around_HP(water, INI_WATER_HP)
        
        self.water_dir_cnt = self.count_water_dir()
    
    # 各座標から見た方角毎の水源の数と距離を基に、水源への行きやすさをスコア化
    def count_water_dir(self):
        water_dir_cnt = [[{"U":0,"L":0,"R":0,"D":0} for _ in range(self.N)] for _ in range(self.N)]
        
        for y in range(self.N):
            for x in range(self.N):
                for water in self.water_pos:
                    for dir in water_dir_cnt[y][x]:
                        if water.y < y and water.x < x and dir in ["D","R"]: continue # 水源がUL方向ならD,Rには進まない
                        elif water.y < y and water.x == x and dir in ["D"]: continue # 水源がU方向ならDには進まない
                        elif water.y < y and water.x > x and dir in ["D","L"]: continue # 水源がUR方向ならD,Lには進まない
                        elif water.y == y and water.x < x and dir in ["R"]: continue # 水源がL方向ならRには進まない
                        elif water.y == y and water.x > x and dir in ["L"]: continue # 水源がR方向ならLには進まない
                        elif water.y > y and water.x < x and dir in ["U","R"]: continue # 水源がDL方向ならU,Rには進まない
                        elif water.y > y and water.x == x and dir in ["U"]: continue # 水源がD方向ならUには進まない
                        elif water.y > y and water.x > x and dir in ["U","L"]: continue # 水源がDR方向ならU,Lには進まない
                        # 水源までの距離が近いほど高スコアとして加算(ただし縦/横のうち距離が遠い方を高スコアにする)
                        if dir in ["U","D"]:
                            water_dir_cnt[y][x][dir] += 1 / (abs(water.y - y) + abs(water.x - x)*2 + 1)
                        elif dir in ["L","R"]:
                            water_dir_cnt[y][x][dir] += 1 / (abs(water.x - x) + abs(water.y - y)*2 + 1)
                        # water_dir_cnt[y][x][dir] += 1 / (abs(water.y - y) + abs(water.x - x) + 1)

        return water_dir_cnt

    # 破壊するまで岩盤を削る
    def destruct(self, pos, power):
        total_damage = 0
        while not self.field.is_broken[pos.y][pos.x]:
            result = self.field.query(pos.y, pos.x, power)
            total_damage += power
            if result == Response.FINISH:
                # print(*self.field.current_HP, sep="\n", file=sys.stderr)
                print(f"# total_cost={self.field.total_cost}")
                sys.exit(0)
            elif result == Response.INVALID:
                print(f"# invalid: y={pos.y} x={pos.x}", file=sys.stderr)
                sys.exit(1)
        # 破壊した岩盤周辺の頑丈さを破壊に要したダメージで更新
        if total_damage > 0:
            self.field.current_HP[pos.y][pos.x] = 0
            self.update_around_HP(pos,total_damage)
        return total_damage

    # 周囲の岩盤の頑丈さを更新
    def update_around_HP(self, pos, new_hp):
        for idx_y, y in enumerate(range(pos.y-AROUND_DIST, pos.y+AROUND_DIST+1)):
            for idx_x, x in enumerate(range(pos.x-AROUND_DIST, pos.x+AROUND_DIST+1)):
                if 0<=y<self.N and 0<=x<self.N and self.field.current_HP[y][x] > 0:
                    # 1.1倍すると何故かスコアが良くなるような…
                    self.field.current_HP[y][x] = new_hp*1.1

    # 周囲の頑丈さの調査ステータスを更新(-1:未調査、0：調査済だが水源には繋がらない、1:調査済で水源に繋がる)
    def update_investigated_area(self, pos, status):
        for dy in range(-AROUND_DIST, AROUND_DIST+1):
            for dx in range(-AROUND_DIST, AROUND_DIST+1):
                ny,nx = pos.y+dy,pos.x+dx
                if 0<=ny<self.N and 0<=nx<self.N:
                    if self.field.is_investigated[ny][nx] == INVESTIGATED_STATUS.CONNECT_TO_WATER:
                        continue
                    elif self.field.is_investigated[ny][nx] == INVESTIGATED_STATUS.INVESTIGATED:
                        if status == INVESTIGATED_STATUS.CONNECT_TO_WATER:
                            self.field.is_investigated[ny][nx] = INVESTIGATED_STATUS.CONNECT_TO_WATER
                    else:
                        self.field.is_investigated[ny][nx] = status

    # NxNのフィールドを平滑化することにより、頑丈さを尤もらしい値に均す
    def smoothing(self):
        dst = [[0]*self.N for _ in range(self.N)]
        d = SMOOTHING_AREA//2
        for y in range(self.N):
            for x in range(self.N):
                cnt = 0
                for dy in range(-d,d+1):
                    for dx in range(-d,d+1):
                        ny,nx = y+dy,x+dx
                        if 0<=ny<self.N and 0<=nx<self.N:
                            dst[y][x] += self.field.current_HP[y+dy][x+dx] * MASK[dy+d][dx+d]
                            cnt += 1
                dst[y][x] *= (SMOOTHING_AREA**2) / cnt
        return dst

    # 各家から水源の周辺に至るまでの周囲の岩盤の頑丈さをDFSで調査する
    def investigate_field(self, pos, start_house, investigated_pos):

        # 水源の周囲まで辿り着いた場合は探索を終了
        for water in self.water_pos:
            if abs(pos.y - water.y) + abs(pos.x - water.x) <= INVESTIGATE_DIST*2:
                # 発見済の水源リストに追加
                self.found_water_pos.add(water)
                # スタート地点の家から水源に至るルートを発見済として更新
                self.is_house_connect_to_water[start_house] = True
                return True
        
        # 水源に繋がる調査済エリアに辿り着いた場合も探索を終了
        for dy in range(-AROUND_DIST, AROUND_DIST+1):
            for dx in range(-AROUND_DIST, AROUND_DIST+1):
                ny,nx = pos.y+dy,pos.x+dx
                if 0<=ny<self.N and 0<=nx<self.N:
                    if self.field.is_investigated[ny][nx] == INVESTIGATED_STATUS.CONNECT_TO_WATER:
                        self.is_house_connect_to_water[start_house] = True
                        return True

        # 今いる地点から見て、より水源に近づけそうな(=スコアが高い)方角から順に探索
        water_dir_score = []
        for key in self.water_dir_cnt[pos.y][pos.x]:
            water_dir_score.append((key, self.water_dir_cnt[pos.y][pos.x][key]))
        water_dir_score.sort(reverse=True, key=lambda x:x[1])

        # 次の調査エリアを決める
        for dir,_ in water_dir_score:
            nxt = Pos(pos.y + DIR[dir][0]*INVESTIGATE_DIST, pos.x + DIR[dir][1]*INVESTIGATE_DIST)
            if (not (0<=nxt.y<self.N and 0<=nxt.x<self.N)) or self.field.is_investigated[nxt.y][nxt.x] != INVESTIGATED_STATUS.NO:
                continue

            # 次に調査するエリアの周辺は調査済とする
            self.update_investigated_area(nxt,INVESTIGATED_STATUS.INVESTIGATED)
            investigated_pos.add(pos)

            total_damage = 0
            for _ in range(self.INVESTIGATE_LOOP):
                total_damage += self.INVESTIGATE_POWER
                # もし岩盤を破壊した場合は、与えたダメージをcurrent_HPに反映
                if self.field.is_broken[nxt.y][nxt.x]:
                    self.field.current_HP[nxt.y][nxt.x] = 0
                    self.update_around_HP(nxt, total_damage)
                    fin_flg = self.investigate_field(nxt, start_house, investigated_pos)
                    if fin_flg:
                        return True
                    break
                else:
                    result = self.field.query(nxt.y, nxt.x, self.INVESTIGATE_POWER)
                    if result == Response.FINISH:
                        print(f"# total_cost={self.field.total_cost}")
                        sys.exit(0)
                    elif result == Response.INVALID:
                        print(f"# invalid: y={nxt.y} x={nxt.x}", file=sys.stderr)
                        sys.exit(1)                    
            else:
                # 岩盤を破壊できなかった場合はcurrent_HPからtotal_damageを引く
                self.field.current_HP[nxt.y][nxt.x] = max(0, self.field.current_HP[nxt.y][nxt.x] - total_damage)

        # 水源が見つからなかった場合はFalse
        return False

    # 水源に至る道が未発見の家から水源に至る調査済エリアを見つけるまで周囲の岩盤の頑丈さをBFSで追加調査する
    def investigate_field_additional(self, start_water, start_time):
        queue = deque([start_water])
 
        while queue:

            # TLE対策
            now = time.time()
            if now - start_time > TIME_LIMIT:
                return

            cur = queue.popleft()

            # あまり遠くまで探索に行きすぎないよう、マンハッタン距離で探索範囲を制限
            if abs(cur.y - start_water.y) + abs(cur.x - start_water.x) >= ADDITIONAL_INVESTIGATE_DIST*5:
                break

            # 一度調査した地点は調査済(水源接続)にする
            self.update_investigated_area(cur,INVESTIGATED_STATUS.CONNECT_TO_WATER)

            # 次の調査エリアを決める
            for dy,dx in MOVE:
                nxt = Pos(cur.y + dy*ADDITIONAL_INVESTIGATE_DIST, cur.x + dx*ADDITIONAL_INVESTIGATE_DIST)
                if not (0<=nxt.y<self.N and 0<=nxt.x<self.N):
                    continue

                # 水源に繋がる調査済エリアに辿り着いた場合探索を終了
                for dy in range(-AROUND_DIST, AROUND_DIST+1):
                    for dx in range(-AROUND_DIST, AROUND_DIST+1):
                        ny,nx = nxt.y+dy,nxt.x+dx
                        if 0<=ny<self.N and 0<=nx<self.N:
                            if self.field.is_investigated[ny][nx] == INVESTIGATED_STATUS.INVESTIGATED:
                                return True

                # 調査済エリア(水源発見済含む)の場合は掘削せずに次の調査エリアへ
                if self.field.is_investigated[nxt.y][nxt.x] != INVESTIGATED_STATUS.NO:
                    queue.append(nxt)
                    continue

                total_damage = 0
                # 追加調査では軟らかい岩盤のみを壊したいので、かける力とループ回数を減らす
                for _ in range(self.ADDITIONAL_INVESTIGATE_LOOP):
                    total_damage += self.ADDITIONAL_INVESTIGATE_POWER
                    # もし破壊済の場合は、破壊情報をcurrent_HPに反映
                    if self.field.is_broken[nxt.y][nxt.x]:
                        self.field.current_HP[nxt.y][nxt.x] = 0
                        self.update_around_HP(nxt,total_damage)
                        queue.append(nxt)
                        break
                    else:
                        result = self.field.query(nxt.y, nxt.x, self.ADDITIONAL_INVESTIGATE_POWER)
                        if result == Response.FINISH:
                            print(f"# total_cost={self.field.total_cost}")
                            sys.exit(0)
                        elif result == Response.INVALID:
                            print(f"# invalid: y={ny} x={nx}", file=sys.stderr)
                            sys.exit(1)
                else:
                    # 岩盤を破壊できなかった場合はcurrent_HPからtotal_damageを引き、次の調査エリアへ
                    self.field.current_HP[nxt.y][nxt.x] = max(0, self.field.current_HP[nxt.y][nxt.x] - total_damage)
                    queue.append(nxt)
 
    def dijkstra(self,d,p,sy,sx):
        hq = [(0, (sy,sx))] # (distance, node)
        seen = [[False]*self.N for _ in range(self.N)] # ノードが確定済みかどうか
        while hq:
            y,x = heappop(hq)[1] # ノードを pop する
            seen[y][x] = True
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if not (0<=ny<self.N and 0<=nx<self.N):
                    continue

                cost = self.field.current_HP[ny][nx]
                if seen[ny][nx] == False and d[y][x] + cost < d[ny][nx]:
                    d[ny][nx] = d[y][x] + cost
                    heappush(hq, (d[ny][nx], (ny, nx)))
                    p[ny][nx] = [y,x]

    #最短経路復元
    def get_path(self,p,ty,tx):
        path = []
        t = [ty,tx]
        while t != [-1,-1]:
            s = p[t[0]][t[1]]
            d = (t[0]-s[0], t[1]-s[1])
            tmp = [k for k, v in DIR.items() if v == d]
            if tmp:
                path.append(*tmp)
            t = s
        path.reverse()
        return path

    def solve(self):
        start = time.time()

        # フェーズ1:水源への行きやすさスコアが高い家から水源に向かってソナーのように頑丈さを調査していく
        # 水源への行きやすさスコアが高い順に家をソート
        house_pos_with_score = []
        for house in self.house_pos:
            water_dir_cnt = []
            for key in self.water_dir_cnt[house.y][house.x]:
                water_dir_cnt.append(self.water_dir_cnt[house.y][house.x][key])
            water_dir_cnt.sort(reverse=True)
            house_pos_with_score.append((house,water_dir_cnt[0]))
        house_pos_with_score.sort(reverse=True, key=lambda x:x[1])

        # 各家からスタートして水源に向かうDFSで周囲の頑丈さを調査
        for house, score in house_pos_with_score:
            now = time.time()
            if now-start > TIME_LIMIT:
                break
            investigated_pos = set()
            fin_flg = self.investigate_field(house, house, investigated_pos)
            # 水源(或いは水源に至る調査済エリア)が見つかって調査終了した場合は、
            # 今回調査したエリアも水源に至る調査済エリアとして更新する
            if fin_flg:
                for pos in investigated_pos:
                    self.update_investigated_area(pos,INVESTIGATED_STATUS.CONNECT_TO_WATER)

        # フェーズ1.5:水源が1つだけで、その水源に至る道がない時の追加調査
        if len(self.water_pos) == 1 and len(self.found_water_pos) == 0:
            for water in self.water_pos:
                fin_flg = self.investigate_field_additional(water, start)
                
        # フェーズ2:フェーズ1で推定したフィールドの頑丈さを平滑化し、未調査エリアの頑丈さを尤もらしい値に均す
        self.field.current_HP = self.smoothing()
        # print(*self.field.current_HP, sep="\n", file=sys.stderr)
        
        # フェーズ3
        # フェーズ1,2で推定したフィールドの頑丈さに従い、ダイクストラで最小コストとなるルートを選択し岩盤を破壊
        # 水源への行きやすさスコアが低い家(≒遠くの家)から順に岩盤破壊
        for house, score in house_pos_with_score[::-1]:
            dist = [[INF]*self.N for _ in range(self.N)]
            dist[house.y][house.x] = 0
            prev =[[[-1,-1]]*self.N for _ in range(self.N)]
            self.dijkstra(dist,prev,house.y,house.x)

            # 最小コストで辿り着ける水源を求める
            min_cost = INF
            min_path = ""
            for water in self.water_pos:
                if dist[water.y][water.x] < min_cost:
                    min_cost = dist[water.y][water.x]
                    min_path = "".join(self.get_path(prev,water.y,water.x))

            # 最小コストで辿り着ける水源までの経路(min_path)上の岩盤を破壊してcurrent_HPを更新
            # 家(岩盤破壊済)から水源まで移動しながら破壊していく
            cur = house
            for dir in min_path:
                cur = Pos(cur.y+DIR[dir][0], cur.x+DIR[dir][1])
                # TODO 過去に岩盤を破壊するのに要した力の差分を元に次に必要な力を予想できないか？
                power = int(max(10, min(MAP_C_DESTRUCT_POWER[self.C], self.field.current_HP[cur.y][cur.x]*0.75 + 1)))
                self.destruct(cur,power)

def main():
    N,W,K,C = map(int,input().split())
    water_pos = []
    house_pos = []
    for _ in range(W):
        y,x = map(int,input().split())
        water_pos.append(Pos(y,x))
    for _ in range(K):
        y,x = map(int,input().split())
        house_pos.append(Pos(y,x))

    solver = Solver(N, water_pos, house_pos, C)
    solver.solve()


if __name__ == "__main__":
    main()
