from enum import Enum
from typing import List
import sys
sys.setrecursionlimit(10**8)
from heapq import heappush, heappop

# 定数
INI_HP = 2500 # 各マスの頑丈さの初期値(仮決め)
INI_HOUSE_HP = 100 # 家周辺の頑丈さの初期値(仮決め)
INI_WATER_HP = 100 # 水源周辺の頑丈さの初期値(仮決め)
AROUND_RANGE = 5 # 家と水源の周辺何マスを初期化するか
SMOOTHING_AREA = 5 # 何マスｘ何マスの平滑化フィルタを作成するか
MASK = [[1/25,1/25,1/25,1/25,1/25],
        [1/25,1/25,1/25,1/25,1/25],
        [1/25,1/25,1/25,1/25,1/25],
        [1/25,1/25,1/25,1/25,1/25],
        [1/25,1/25,1/25,1/25,1/25]]

INVESTIGATE_COUNT = 100
INVESTIGATE_POWER = 100
CONNECT_POWER = 100
DIR = {"U":(-1,0), "R":(0,1), "D":(1,0), "L":(0,-1)}
INF = 10**18

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
        self.is_broken = [[False] * N for _ in range(N)]
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

        # 家の周囲の頑丈さをINI_HOUSE_HPで初期化
        # TODO 最初に家を破壊して、そのコストから周囲の頑丈さを初期化
        for house in self.house_pos:
            for y in range(house.y-AROUND_RANGE, house.y+AROUND_RANGE+1):
                for x in range(house.x-AROUND_RANGE, house.x+AROUND_RANGE+1):
                    if 0<=y<self.N and 0<=x<self.N:
                        self.field.current_HP[y][x] = INI_HOUSE_HP

        # 水源の周囲の頑丈さをINI_WATER_HPで初期化
        # TODO 最初に水源を破壊して、そのコストから周囲の頑丈さを初期化
        for water in self.water_pos:
            for y in range(water.y-AROUND_RANGE, water.y+AROUND_RANGE+1):
                for x in range(water.x-AROUND_RANGE, water.x+AROUND_RANGE+1):
                    if 0<=y<self.N and 0<=x<self.N:
                        self.field.current_HP[y][x] = INI_WATER_HP

    # NxNのフィールドを平滑化することにより、頑丈さを尤もらしい値に更新
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
                dst[y][x] *= SMOOTHING_AREA**2 / cnt
        return dst

    # 各家から水源の周辺に至るまでの周囲の岩盤の頑丈さを調査する
    def investigate_field(self, pos, waters, seen):
        # 再帰的に周囲の岩盤を調査していく
        for dy in range(-1,2):
            for dx in range(-1,2):
                ny,nx = pos.y + dy*SMOOTHING_AREA, pos.x + dx*SMOOTHING_AREA
                if not (0<=ny<self.N and 0<=nx<self.N) or seen[ny][nx]:
                    continue

                # 水源の周囲まで辿り着いた場合は探索を終了
                for water in waters:
                    if abs(pos.y - water.y) + abs(pos.x - water.x) <= SMOOTHING_AREA*2:
                        return

                total_damage = 0
                seen[ny][nx] = True
                for _ in range(INVESTIGATE_COUNT):
                    # もし破壊済の場合は、破壊情報をcurrent_HPに反映
                    if self.field.is_broken[ny][nx]:
                        self.field.current_HP[ny][nx] = 0
                        self.investigate_field(Pos(ny,nx), waters, seen)
                        break
                    else:
                        result = self.field.query(ny, nx, INVESTIGATE_POWER)
                        total_damage += INVESTIGATE_POWER
                        if result == Response.FINISH:
                            print(f"# total_cost={self.field.total_cost}")
                            sys.exit(0)
                        elif result == Response.INVALID:
                            print(f"# invalid: y={y} x={x}", file=sys.stderr)
                            sys.exit(1)                    
                else:
                    # 岩盤を破壊できなかった場合はcurrent_HPからtotal_damageを引く
                    # TODO 仮にINI_HPが低い値の場合、current_HPが0から減らせなくなり情報が欠落してしまう。
                    self.field.current_HP[ny][nx] = max(0, self.field.current_HP[ny][nx] - total_damage)

    def dijkstra(self,d,p,sy,sx):
        hq = [(0, (sy,sx))] # (distance, node)
        seen = [[False]*self.N for _ in range(self.N)] # ノードが確定済みかどうか
        while hq:
            y,x = heappop(hq)[1] # ノードを pop する
            seen[y][x] = True
            for dir in DIR:
                ny,nx = y+DIR[dir][0],x+DIR[dir][1]
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
        # フェーズ1
        # print("# phase1",file=sys.stderr)
        # まずは各家の周囲から水源に向かってソナーのように頑丈さを調査していく
        seen = [[False]*self.N for _ in range(self.N)]
        for house in self.house_pos:
            self.investigate_field(house, self.water_pos, seen)
            # その際に、NxNのフィールドを平滑化することにより、頑丈さを尤もらしい値に更新していく
            self.field.current_HP = self.smoothing()
            # 各家について、何をもって探索完了とするか？
            # ⇒まずは、1つの水源の周囲にたどり着くことを探索完了の条件とする。
            # ⇒他にも、あるコスト以下の道が見つかるまで探索を続ける、複数の水源を探索する等工夫の余地あり。

        # フェーズ2
        # print("# phase2",file=sys.stderr)
        # フェーズ1で作成した頑丈さの地図に従い、ダイクストラで最小コストとなるルートを選択し岩盤を破壊
        for house in self.house_pos:
            dist = [[INF]*self.N for _ in range(self.N)]
            dist[house.y][house.x] = 0
            prev =[[[-1,-1]]*self.N for _ in range(self.N)]
            self.dijkstra(dist,prev,house.y,house.x)

            min_cost = INF
            min_path = ""
            for water in self.water_pos:
                if dist[water.y][water.x] < min_cost:
                    min_cost = dist[water.y][water.x]
                    min_path = "".join(self.get_path(prev,water.y,water.x))

            # 最小コストで辿り着ける水源までの経路(min_path)上の岩盤を破壊してcurrent_HPを更新
            # まずはスタート地点となる家の岩盤を破壊
            cur = house
            while not self.field.is_broken[cur.y][cur.x]:
                result = self.field.query(cur.y, cur.x, CONNECT_POWER)
                if result == Response.FINISH:
                    print(f"# total_cost={self.field.total_cost}")
                    sys.exit(0)
                elif result == Response.INVALID:
                    print(f"# invalid: y={cur.y} x={cur.x}", file=sys.stderr)
                    sys.exit(1)
            self.field.current_HP[cur.y][cur.x] = 0

            # 家から水源まで移動しながら破壊していく
            for dir in min_path:
                cur = Pos(cur.y+DIR[dir][0], cur.x+DIR[dir][1])
                while not self.field.is_broken[cur.y][cur.x]:
                    result = self.field.query(cur.y, cur.x, CONNECT_POWER)
                    if result == Response.FINISH:
                        print(f"# total_cost={self.field.total_cost}")
                        sys.exit(0)
                    elif result == Response.INVALID:
                        print(f"# invalid: y={cur.y} x={cur.x}", file=sys.stderr)
                        sys.exit(1)
                self.field.current_HP[cur.y][cur.x] = 0

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
