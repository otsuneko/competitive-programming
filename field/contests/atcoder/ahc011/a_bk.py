import time
import random
from collections import deque
from collections import defaultdict
from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport
import sys
sys.setrecursionlimit(10**7)

# 定数
SEARCH_AREA = 5
DIR = ["D","R","U","L"]
MOVE = {"D":[1, 0], "R":[0, 1], "U":[-1, 0], "L":[0, -1]}
# 各タイルごとに接続可能な方向(上下左右)
TILE_CONNECT = {
    "0":set(),
    "1":{"L"},
    "2":{"U"},
    "3":{"U","L"},
    "4":{"R"},
    "5":{"L","R"},
    "6":{"R","U"},
    "7":{"R","U","L"},
    "8":{"D"},
    "9":{"D","L"},
    "a":{"D","U"},
    "b":{"D","U","L"},
    "c":{"D","R"},
    "d":{"D","R","L"},
    "e":{"D","R","U"},
    "f":{"D","R","U","L"}
}
# 分岐の多いタイルほど中央に近づくように(ゴール配置決定時に使用)
TILE_SCORE = {"0":0,"1":1,"2":1,"3":2,"4":1,"5":2,"6":2,"7":3,"8":1,"9":2,"a":2,"b":3,"c":2,"d":3,"e":3,"f":4}
# タイルを16進数から枝の表示に変換するための辞書
TILE_SHAPE = {"0":"","1":"- ","2":"|","3":"┘","4":" -","5":"－","6":"└","7":"┴","8":"｜","9":"┐","a":"｜","b":"┤","c":"┌","d":"┬","e":"├","f":"┼"}

# タイルを16進数表記からスコア表記に変換、その二次元累積和を返す
def translate_tiles_score(tiles):

    # タイルをスコア表記に変換
    tiles_score = [[0]*N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            tiles_score[y][x] = TILE_SCORE[tiles[y][x]]
    
    # print(*tiles_score, sep="\n")

    # タイルスコアの二次元累積和を計算
    cumsum = [[0]*(N+1) for _ in range(N+1)]
    for y in range(N):
        for x in range(N):
            cumsum[y+1][x+1] = cumsum[y][x+1] + cumsum[y+1][x] - cumsum[y][x] + tiles_score[y][x]
    
    return cumsum

# 0のタイルを含むどのSEARCH_AREA領域を探索範囲にするか
def find_tile_area(cumsum_tiles_score):
    
    # 0のタイルを探す
    Y0,X0 = [0,0]
    for y in range(N):
        for x in range(N):
            if tiles[y][x] == "0":
                Y0,X0 = y,x
                break

    # 0のタイルを含むどの領域を探索範囲にするか
    max_score = 0
    max_area = [0,0,0,0]
    for y1 in range(N):
        for x1 in range(N):
            y2,x2 = y1+SEARCH_AREA,x1+SEARCH_AREA
            if not (0<=y1<N and 0<=x1<N and y1<=Y0<y2 and x1<=X0<x2):
                continue
            score = cumsum_tiles_score[y2][x2] - cumsum_tiles_score[y2][x1-1] - cumsum_tiles_score[y1-1][x2] + cumsum_tiles_score[y1-1][x1-1]
            
            if score > max_score:
                max_score = score
                max_area = [y1,x1,y2,x2]

    return max_area

# 2つのタイルが繋がっているか判定
def is_tile_connected(ntile,dir):
    if (dir == "D" and "U" in ntile) or (dir == "R" and "L" in ntile) or (dir == "U" and "D" in ntile) or (dir == "L" and "D" in ntile):
        return True
    return False

# 最大の木のサイズをDFSで計算
def calc_max_tree(tiles):

    seen = [[False]*N for _ in range(N)]
    size = 0

    # 木のサイズを計算
    def calc_tree_size(y,x,seen):
        size = 0
        seen[y][x] = True
        edge = TILE_CONNECT[tiles[y][x]]
        for dir in DIR:
            # 次のタイルに向かう枝が伸びていない場合はスキップ
            if dir not in edge:
                continue
            ny,nx = y+MOVE[dir][0],x+MOVE[dir][1]
            if not (0<=ny<N and 0<=nx<N and not seen[ny][nx]):
                continue
            if is_tile_connected(TILE_CONNECT[tiles[ny][nx]],dir):
                size += calc_tree_size(ny,nx,seen) + 1

        return size

    # 最大の木のサイズを計算
    max_tree_size = 1
    for y in range(N):
        for x in range(N):
            if not seen[y][x]:
                max_tree_size = max(max_tree_size, calc_tree_size(y,x,seen))

    return max_tree_size

# タイルの深いコピー
def copy_tiles(tiles):
    new_tiles = [[""]*N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            new_tiles[y][x] = tiles[y][x]
    return new_tiles

# フェーズ1：与えられたタイルを基に作れる極力大きい木を探索(ゴール配置の決定)
# 極力大きい木を山登りで探索
def find_goal_state(tiles, tiles_score):
    # 0のタイルを含むどのSEARCH_AREAを探索範囲にするか
    search_area = find_tile_area(tiles_score)

    # 初期値生成
    # タイルの枝の数を基にして、枝が多いものほど中央に配置されるように初期値生成
    # ランダムに2タイルを選んで2回交換する山登り
    # TODO: 後で焼きなましに変える
    y1,x1,y2,x2 = search_area
    max_tree_size = 0
    goal_tiles = [[""]*N for _ in range(N)] # タイルのゴール配置
    while 1:
        now = time.time()
        if now - start > 1.5:
            break
        # 2タイルを選んで交換を2回繰り返す(1回だと解けないパズルになる)
        for _ in range(2):
            # 入れ替える2タイルの位置を乱数で決定(同じ位置のタイルは入れ替えと認めない)
            while 1:
                sy,sx = random.randint(y1,y2-1), random.randint(x1,x2-1)
                ty,tx = random.randint(y1,y2-1), random.randint(x1,x2-1)
                if [sy,sx] != [ty,tx]:
                    break
            # タイルの入れ替え
            tiles[sy][sx],tiles[ty][tx] = tiles[ty][tx],tiles[sy][sx]
        # 入れ替え後のスコア(最大の木のサイズ)をDFSで計算
        size = calc_max_tree(tiles)

        if size > max_tree_size:
            max_tree_size = size
            goal_tiles = copy_tiles(tiles)

        tiles = copy_tiles(goal_tiles)

    # print(max_tree_size)
    # print(*goal_tiles, sep="\n")
    # print_tiles(goal_tiles)

    return goal_tiles

# フェーズ2：フェーズ1で発見したゴール配置に至るまでの最短手数の探索をA*で実施
# dist：当該タイル配置に至るまでの最短手数、cost：dist + 当該タイル配置からゴール配置までの推定コスト(＜実コスト)
def solve_puzzle(start_tiles,goal_tiles):

    queue = []          # 待ち行列
    dist_dic = defaultdict(int)       # 初期タイル配置からの手数
    operation_dic = defaultdict(list)   # 当該タイル配置に至るまでの操作手順
    initial_dist = 0    # 初期配置から当該配置に至るまでの最短手数
    initial_cost = initial_dist + calc_heuristic(start_tiles, goal_tiles)     # 初期タイル配置でのゴール配置までの推定コスト
    pos_zero = start_tiles.index("0")   # 0のタイルがどこにあるか
    operation = tuple([])  # 当該盤面を構築するまでの手順(0のタイルの上下左右どれと入れ替えるか)
    heappush(queue, (initial_cost,initial_dist,start_tiles,pos_zero,operation))

    # ゴールに到達するまで新しい盤面を探索する
    while queue:
        # ゴール配置までの距離最小のタイル配置を取り出す
        cur_cost,cur_dist,cur_tiles,cur_pos_zero,cur_operation = heappop(queue)
        # print(len(dist_dic))

        # ゴール配置と一致したら終了
        if cur_tiles == goal_tiles:
            return operation_dic[cur_tiles]

        # 次の配置を探索(0に上下左右で隣接するタイルを動かす)
        for dir in DIR:
            # 0の上下左右タイルを探索
            new_pos_zero = cur_pos_zero + MOVE[dir][0]*N + MOVE[dir][1]
            # 新規tilesインスタンスの作成、タイル入れ替え
            if 0<=new_pos_zero<N*N:
                # 0タイルと隣接タイルの入れ替え
                new_tiles = list(cur_tiles)[:]
                new_tiles[cur_pos_zero],new_tiles[new_pos_zero] = new_tiles[new_pos_zero],new_tiles[cur_pos_zero]
                # 操作手順の追加
                new_operation = list(cur_operation)[:]
                new_operation.append(dir)
                new_dist = cur_dist + 1

                # ゴール配置までの推定コストの計算
                new_cost = new_dist + calc_heuristic(new_tiles,goal_tiles)

                new_tiles = tuple(new_tiles)
                new_operation = tuple(new_operation)
                # new_tilesが未到達の配置 or 到達済だがよりゴール配置に近ければ更新
                if not (dist_dic[new_tiles] == 0 or new_cost < dist_dic[new_tiles]):
                    continue
                # より少ない手数でnew_tilesに到達できる場合は更新
                if not (not operation_dic[new_tiles] or len(new_operation) < len(operation_dic[new_tiles])):
                    continue
                dist_dic[new_tiles] = new_cost
                operation_dic[new_tiles] = new_operation[:]
                heappush(queue, (new_cost, new_dist, new_tiles, new_pos_zero, new_operation))

    return []

# 現在のタイル配置からゴール配置までの推定コスト(＜実コスト)を計算する
def calc_heuristic(cur_tiles,goal_tiles):

    # あるタイルと同じ種類かつまだ選ばれていないタイルのうち最も近いものを探索(マンハッタン距離計算用)
    def search_nearest_tile(sidx,cur_tiles,goal_tiles,used):
        seen = [False]*(N*N)
        seen[sidx] = True
        tile = cur_tiles[sidx]
        queue = deque([(sidx,0)])
        while queue:
            idx,manhattan = queue.popleft()
            ntile = goal_tiles[idx]
            if tile == ntile and idx not in used:
                used.add(idx)
                return manhattan
            for dir in DIR:
                nidx = idx + MOVE[dir][0]*N + MOVE[dir][1]
                if 0<=nidx<N*N and not seen[nidx]:
                    seen[nidx] = True
                    queue.append((nidx,manhattan+1))
        return 0

    used = set() # 既に距離計算に使用された、ゴール配置のタイル
    cost = 0 # ゴール盤面までの推定コスト(同じ番号を持つスタート/ゴールのタイルペアのマンハッタン距離の和)
    # 同じ番号を持つスタート/ゴールのタイルペアで、同じ座標のものをusedに追加
    same = 0
    for idx in range(N*N):
        if cur_tiles[idx] == goal_tiles[idx]:
            used.add(idx)
            same += 1

    for idx in range(N*N):
        if cur_tiles[idx] != goal_tiles[idx]:
            # print(used)
            cost += search_nearest_tile(idx,cur_tiles,goal_tiles,used)

    print(same)
    return same+cost
    return cost*1.9

# タイルを16進数から枝の表示に変換して表示(デバッグ用)
def print_tiles(tiles):
    new_tiles = [[""]*N for _ in range(N)]
    # タイルを16進数から枝の表示に変換
    for y in range(N):
        for x in range(N):
            new_tiles[y][x] = TILE_SHAPE[tiles[y][x]]
        print("".join(new_tiles[y]))    


# 入力
N,T = map(int,input().split()) # 6 <= N <= 10, T = 2 * N**3
tiles = [list(input()) for _ in range(N)]
# print(*tiles,sep="\n")

# 変数
start = time.time()

# メイン処理
# フェーズ1：与えられたタイルを基に作れる極力大きい木を探索(ゴール配置の決定)
cumsum_tiles_score = translate_tiles_score(tiles)
goal_tiles = find_goal_state(tiles, cumsum_tiles_score)

# フェーズ2：フェーズ1で発見したゴール配置に至るまでの最短手数の探索
# フェーズ2からは、タイル配置を2次元→1次元化する
start_tiles_1d, goal_tiles_1d = [],[]
for y in range(N):
    start_tiles_1d += tiles[y]
    goal_tiles_1d += goal_tiles[y]
ans = solve_puzzle(tuple(start_tiles_1d),tuple(goal_tiles_1d))
print("".join(ans))