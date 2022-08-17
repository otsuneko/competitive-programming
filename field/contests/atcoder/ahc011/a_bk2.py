import time
import random
import math
import sys
sys.setrecursionlimit(10**7)

# 定数
DIR = ["D","R","U","L"]
REVERSE_DIR = {"D":"U","R":"L","U":"D","L":"R"}
MOVE = {"D":[1, 0], "R":[0, 1], "U":[-1, 0], "L":[0, -1]}
CHECK_SPAN = {6:20,7:30,8:40,9:40,10:40} # このターン数経過ごとに、木のサイズが更新されているかをチェック(Nに応じて変化)
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
# 枝の多いタイルほど中央に近づくようにするヒューリスティックスコア計算用定数
TILE_SCORE = {"0":0,"1":1,"2":1,"3":2,"4":1,"5":2,"6":2,"7":3,"8":1,"9":2,"a":2,"b":3,"c":2,"d":3,"e":3,"f":4}
# 中央に近いほど重みが大きくなる分布図
SCORE_DISTRIBUTION = {
    6:(1,1,1,1,1,1,1,2,2,2,2,1,1,2,3,3,2,1,1,2,3,3,2,1,1,2,2,2,2,1,1,1,1,1,1,1),
    7:(1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,2,3,3,3,2,1,1,2,3,4,3,2,1,1,2,3,3,3,2,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1),
    8:(1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,1,1,2,3,3,3,3,2,1,1,2,3,4,4,3,2,1,1,2,3,4,4,3,2,1,1,2,3,3,3,3,2,1,1,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1),
    9:(1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,2,3,3,3,3,3,2,1,1,2,3,4,4,4,3,2,1,1,2,3,4,5,4,3,2,1,1,2,3,4,4,4,3,2,1,1,2,3,3,3,3,3,2,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1),
    10:(1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,2,3,3,3,3,3,3,2,1,1,2,3,4,4,4,4,3,2,1,1,2,3,4,5,5,4,3,2,1,1,2,3,4,5,5,4,3,2,1,1,2,3,4,4,4,4,3,2,1,1,2,3,3,3,3,3,3,2,1,1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1)
}
# タイルを16進数から枝の表示に変換するための辞書
TILE_SHAPE = {"0":"","1":"- ","2":"|","3":"┘","4":" -","5":"－","6":"└","7":"┴","8":"｜","9":"┐","a":"｜","b":"┤","c":"┌","d":"┬","e":"├","f":"┼"}
# 焼きなましパラメータ
# START_TEMP = 2
# END_TEMP = 2
TIME_LIMIT = 2.8

# 2つのタイルが繋がっているか判定
def is_tile_connected(ntile,dir_n):
    if DIR[(dir_n+2)%4] in ntile:
        return True
    return False

# 最大の木のサイズをDFSで計算
def calc_max_tree(tiles):

    # 木のサイズを計算
    def calc_tree_size(idx,seen):
        size = 0
        seen[idx] = True
        for dir_n in range(4):
            dir = DIR[dir_n]
            # 次のタイルに向かう枝が伸びていない場合はスキップ
            if dir not in TILE_CONNECT[tiles[idx]]:
                continue
            # 不正な操作を除外(左端から左へ移動or右端から右へ移動)
            if (idx%N == 0 and dir == "L") or (idx%N == N-1 and dir == "R"):
                continue
            nidx = idx + MOVE[dir][0]*N + MOVE[dir][1]
            if 0<=nidx<N*N and not seen[nidx]:
                if is_tile_connected(TILE_CONNECT[tiles[nidx]],dir_n):
                    # print(idx,nidx,tiles[idx],tiles[nidx],dir)
                    size += calc_tree_size(nidx,seen)+1

        return size

    # 最大の木のサイズを計算
    max_tree_size = 1
    seen = [False]*(N*N)
    for idx in range(N*N):
        if not seen[idx]:
            max_tree_size = max(max_tree_size, calc_tree_size(idx,seen)+1)

    return max_tree_size

# 0タイルの移動方向を決定
def decide_move_dir(cur_tiles):

    cand_dir = ["D","R","U","L"]
    # 1個前の状態に戻る移動は除外
    if cur_tiles.pre_dir != "":
        cand_dir.remove(REVERSE_DIR[cur_tiles.pre_dir])

    # 不正な操作(範囲の外への移動)を除外
    if cur_tiles.tile_zero >= N*(N-1) and "D" in cand_dir:
        cand_dir.remove("D")
    if cur_tiles.tile_zero < N and "U" in cand_dir:
        cand_dir.remove("U")
    if cur_tiles.tile_zero%N == 0 and "L" in cand_dir:
        cand_dir.remove("L")
    if cur_tiles.tile_zero%N == N-1 and "R" in cand_dir:
        cand_dir.remove("R")

    dir = random.choice(cand_dir)

    return dir

# タイルステータス管理用クラス
class TileStatus:

    def __init__(self,tiles,tile_zero,tree_size,operation,turn,pre_dir):
        self.tiles = tiles[:] # タイル配置
        self.tile_zero = tile_zero # 0タイルの位置
        self.tree_size = tree_size # 最大の木のサイズ
        self.operation = operation[:] # 操作手順(0タイルを上下左右どの方向に動かすか)
        self.turn = turn # 当該タイル配置を作るのに要するターン数
        self.pre_dir = pre_dir # 1手前の0タイルの移動方向
        self.score = 0 # 木のサイズに応じたスコア
        self.heuristic_score = 0 # タイル配置の良さを表すヒューリスティックスコア(中央に枝の多いタイルが多いほど高くなる)
    
    def copy(self,new_tiles):
        self.tiles = new_tiles.tiles[:] # タイル配置
        self.tile_zero = new_tiles.tile_zero # 0タイルの位置
        self.tree_size = new_tiles.tree_size # 最大の木のサイズ
        self.operation = new_tiles.operation[:] # 操作手順(0タイルを上下左右どの方向に動かすか)
        self.turn = new_tiles.turn # 当該タイル配置を作るのに要するターン数
        self.pre_dir = new_tiles.pre_dir # 1手前の0タイルの移動方向
        self.score = new_tiles.score # 木のサイズに応じたスコア
        self.heuristic_score = new_tiles.heuristic_score # タイル配置の良さを表すヒューリスティックスコア(中央に枝の多いタイルが多いほど高くなる)
    
    def switch_tiles(self,dir):
        new_tile_zero = self.tile_zero + MOVE[dir][0]*N + MOVE[dir][1]
        self.tiles[self.tile_zero],self.tiles[new_tile_zero] = self.tiles[new_tile_zero],self.tiles[self.tile_zero]
        self.tile_zero = new_tile_zero
        self.pre_dir = dir
        self.operation.append(dir)
        self.tree_size = calc_max_tree(self.tiles) # 入れ替え後のスコア(最大の木のサイズ)をDFSで計算
        # self.score = self.calc_score()
        self.heuristic_score = self.calc_heuristic_score()

    # タイルを16進数から枝の表示に変換して表示(デバッグ用)
    def print_tiles(self):
        # タイルを16進数から枝の表示に変換
        row = []
        for idx in range(N*N):
            row.append(TILE_SHAPE[self.tiles[idx]])
            if idx > 0 and idx%(N-1) == 0:
                print("".join(row))
                row = []

    # スコア計算
    def calc_score(self):
        S = self.tree_size
        K = self.turn
        score = 0
        if S < N*N-1:
            score = round(500000*S/(N*N-1))
        else:
            score = round(500000*(2-(K/T)))
        return score
    
    # ヒューリスティックスコア計算
    def calc_heuristic_score(self):
        heuristic_score = 0
        for idx in range(N*N):
            heuristic_score += TILE_SCORE[self.tiles[idx]] * SCORE_DISTRIBUTION[N][idx]
        heuristic_score = heuristic_score**0.5
        return heuristic_score

# 温度関数
# def temperature(now):
#     x = now / TIME_LIMIT
#     ret = pow(START_TEMP, 1-x) * pow(END_TEMP, x)
#     return ret

# 焼きなましのスコア低下受け入れ確率
# def prob(score, new_score):
#     diff = new_score - score
#     prob = math.exp(diff / temperature(time.time()-start))
#     return prob

# 最大の大きさの木を探索
def solve(tiles):

    # 2セット盤面を用意し、ベストを残していく
    cur_tiles = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="")
    cur_tiles2 = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="")
    best_tiles = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="")
    best_tiles2 = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="")
    checkpoint_tiles = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="")
    checkpoint_tiles2 = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="")
    turn = pre_turn = 0
    turn2 = pre_turn2 = 0

    while turn < T:
        now = time.time()
        if now - start > TIME_LIMIT:
            if best_tiles.tree_size > best_tiles2.tree_size:
                return best_tiles
            else:
                return best_tiles2

        # タイルの入れ替え
        # 入れ替え方向の決定
        dir = decide_move_dir(cur_tiles)
        dir2 = decide_move_dir(cur_tiles2)

        # タイル入れ替え
        cur_tiles.switch_tiles(dir)
        cur_tiles2.switch_tiles(dir2)

        # 最善の状態をコピー
        if cur_tiles.tree_size * cur_tiles.heuristic_score > best_tiles.tree_size * best_tiles.heuristic_score:
            best_tiles.copy(cur_tiles)
            pre_turn = turn

        if cur_tiles2.tree_size * cur_tiles2.heuristic_score > best_tiles2.tree_size * best_tiles2.heuristic_score:
            best_tiles2.copy(cur_tiles2)
            pre_turn2 = turn2

        # 一定ターンごとに木のサイズが大きくなったかを判定、なってなければやり直し
        if turn == pre_turn + CHECK_SPAN[N]:
            if best_tiles.tree_size * best_tiles.heuristic_score > checkpoint_tiles.tree_size * checkpoint_tiles.heuristic_score:
                # 前のチェックポイントより良くなった場合はベスト地点からやり直し
                cur_tiles.copy(best_tiles)
                turn = pre_turn = best_tiles.turn
            else:
                # 良くなってない場合前のチェックポイントからやり直し
                cur_tiles.copy(checkpoint_tiles)
                turn = pre_turn = checkpoint_tiles.turn
            checkpoint_tiles.copy(cur_tiles)

        if turn2 == pre_turn2 + CHECK_SPAN[N]:
            if best_tiles2.tree_size * best_tiles2.heuristic_score > checkpoint_tiles2.tree_size * checkpoint_tiles2.heuristic_score:
                # 前のチェックポイントより良くなった場合はベスト地点からやり直し
                cur_tiles2.copy(best_tiles2)
                turn2 = pre_turn2 = best_tiles2.turn
            else:
                # 良くなってない場合前のチェックポイントからやり直し
                cur_tiles2.copy(checkpoint_tiles2)
                turn2 = pre_turn2 = checkpoint_tiles2.turn
            checkpoint_tiles2.copy(cur_tiles2)

        # if max(turn,turn2) > T//2:
        #     if best_tiles.tree_size > best_tiles2.tree_size:
        #         cur_tiles.copy(best_tiles)
        #         cur_tiles2.copy(best_tiles)
        #         turn = pre_turn = turn2 = pre_turn2 = best_tiles.turn
        #     else:
        #         cur_tiles.copy(best_tiles2)
        #         cur_tiles2.copy(best_tiles2)
        #         turn = pre_turn = turn2 = pre_turn2 = best_tiles2.turn
        #     checkpoint_tiles.copy(cur_tiles)
        #     checkpoint_tiles2.copy(cur_tiles2)

        turn += 1
        turn2 += 1

    if best_tiles.tree_size > best_tiles2.tree_size:
        return best_tiles
    else:
        return best_tiles2

# 入力
N,T = map(int,input().split()) # 6 <= N <= 10, T = 2 * N**3
tiles = []
for _ in range(N):
    tiles += list(input())
# print(tiles)

# 変数
start = time.time()

# メイン処理
best_tiles = solve(tiles)
# print(best_tiles.calc_score())
# print(best_tiles.print_tiles())
print("".join(best_tiles.operation))