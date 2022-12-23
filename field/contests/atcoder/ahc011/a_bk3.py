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
# ビームサーチパラメータ
BEAM_RANGE = 75

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

# 移動可能な0タイルの移動方向を探索
def search_movable_dirs(cur_tiles):

    cand_dirs = ["D","R","U","L"]
    # 1個前の状態に戻る移動は除外
    if cur_tiles.pre_dir != "":
        cand_dirs.remove(REVERSE_DIR[cur_tiles.pre_dir])

    # 不正な操作(範囲の外への移動)を除外
    if cur_tiles.tile_zero >= N*(N-1) and "D" in cand_dirs:
        cand_dirs.remove("D")
    if cur_tiles.tile_zero < N and "U" in cand_dirs:
        cand_dirs.remove("U")
    if cur_tiles.tile_zero%N == 0 and "L" in cand_dirs:
        cand_dirs.remove("L")
    if cur_tiles.tile_zero%N == N-1 and "R" in cand_dirs:
        cand_dirs.remove("R")

    return cand_dirs

# タイルステータス管理用クラス
class TileStatus:

    def __init__(self,tiles,tile_zero,tree_size,operation,turn,pre_dir,score,heuristic_score):
        self.tiles = tiles[:] # タイル配置
        self.tile_zero = tile_zero # 0タイルの位置
        self.tree_size = tree_size # 最大の木のサイズ
        self.operation = operation[:] # 操作手順(0タイルを上下左右どの方向に動かすか)
        self.turn = turn # 当該タイル配置を作るのに要するターン数
        self.pre_dir = pre_dir # 1手前の0タイルの移動方向
        self.score = score # 木のサイズに応じたスコア
        self.heuristic_score = heuristic_score # タイル配置の良さを表すヒューリスティックスコア(中央に枝の多いタイルが多いほど高くなる)
    
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
        self.heuristic_score = 1
        # self.heuristic_score = self.calc_heuristic_score()
        # self.heuristic_score = self.calc_heuristic_penalty()

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
    # def calc_heuristic_score(self):
    #     heuristic_score = 0
    #     for idx in range(N*N):
    #         heuristic_score += TILE_SCORE[self.tiles[idx]] * SCORE_DISTRIBUTION[N][idx]
    #     heuristic_score = heuristic_score**0.5
    #     return heuristic_score
    
    # def calc_heuristic_penalty(self):
    #     penalty = 1
    #     for idx in range(N*N):
    #         # 領域の外側に向かって伸びている枝があればペナルティ追加
    #         if idx >= N*(N-1) and "D" in TILE_CONNECT[self.tiles[idx]]:
    #             penalty += 1
    #         if idx < N and "U" in TILE_CONNECT[self.tiles[idx]]:
    #             penalty += 1
    #         if idx%N == 0 and "L" in TILE_CONNECT[self.tiles[idx]]:
    #             penalty += 1
    #         if idx%N == N-1 and "R" in TILE_CONNECT[self.tiles[idx]]:
    #             penalty += 1
    #     return penalty

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

# 最大の大きさの木をビームサーチで探索
def solve_beam_search(tiles):

    # 探索候補の盤面をリストで管理
    ini_tiles = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="",score=0,heuristic_score=1)
    cand_tiles = [ini_tiles]
    best_tiles = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="",score=0,heuristic_score=1)
    visited = {tuple(tiles):ini_tiles} # 到達済みの盤面保存用
    turn = 0

    while turn < T:
        now = time.time()
        if now - start > TIME_LIMIT:
            # print("TLE")
            return best_tiles

        # 探索候補の各盤面について変更可能状態を探索
        new_cand_tiles = []
        for tiles in cand_tiles:
            
            # 0タイルの移動可能な方向それぞれについて状態を変化
            dirs = search_movable_dirs(tiles)
            for dir in dirs:
                new_tiles = TileStatus(tiles.tiles,tiles.tile_zero,tiles.tree_size,tiles.operation,tiles.turn,tiles.pre_dir,tiles.score,tiles.heuristic_score)
                # タイル入れ替え
                new_tiles.switch_tiles(dir)

                # 到達済みの盤面ならやり直し
                key = tuple(new_tiles.tiles)
                if key in visited:
                    continue
                visited[key] = new_tiles
                
                # 探索候補の盤面に盤面を追加
                new_cand_tiles.append(new_tiles)

                # 最善の状態をコピー
                if new_tiles.tree_size > best_tiles.tree_size:
                    best_tiles.copy(new_tiles)

        # 探索候補の盤面から上位BEAM_RANGE個を残す
        cand_tiles = new_cand_tiles
        # if turn%CHECK_SPAN[N]:
        if turn%5:
            new_cand_tiles.sort(reverse=True,key=lambda t:t.tree_size*t.heuristic_score)
            cand_tiles = new_cand_tiles[:BEAM_RANGE]

        turn += 1

    return best_tiles


# 最大の大きさの木を山登りで探索
def solve_climbing(tiles):

    cur_tiles = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="",score=0,heuristic_score=1)
    best_tiles = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="",score=0,heuristic_score=1)
    checkpoint_tiles = TileStatus(tiles=tiles,tile_zero=tiles.index("0"),tree_size=1,operation=[],turn=0,pre_dir="",score=0,heuristic_score=1)
    turn = pre_turn = 0

    while turn < T:
        now = time.time()
        if now - start > TIME_LIMIT:
            return best_tiles
            
        # タイルの入れ替え
        # 入れ替え方向の決定
        dir = decide_move_dir(cur_tiles)

        # タイル入れ替え
        cur_tiles.switch_tiles(dir)

        # 最善の状態をコピー
        if cur_tiles.tree_size * cur_tiles.heuristic_score > best_tiles.tree_size * best_tiles.heuristic_score:
            best_tiles.copy(cur_tiles)
            pre_turn = turn

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

        turn += 1

    return best_tiles


# 入力
N,T = map(int,input().split()) # 6 <= N <= 10, T = 2 * N**3
tiles_in = []
for _ in range(N):
    tiles_in += list(input())
# print(tiles)

# 変数
start = time.time()

# メイン処理
if N == 6:
    best_tiles = solve_beam_search(tiles_in)
else:
    best_tiles = solve_climbing(tiles_in)
print(best_tiles.calc_score())
# print(best_tiles.print_tiles())
print("".join(best_tiles.operation))