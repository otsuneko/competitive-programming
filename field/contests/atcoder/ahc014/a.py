import random
import sys
import time
from copy import deepcopy
from collections import defaultdict

# 定数
TIME_LIMIT = 15
MAX_DIST = 20

# 計測開始
start = time.time()

# 入力
N,M = map(int,input().split())
C = (N-1)//2
pts = set([tuple(map(int,input().split())) for _ in range(M)])
ans = []

# 既に線分が引かれている場所の管理
used = [[[False]*8 for _ in range(N)] for _ in range(N)]

# スコア計算の前処理
S = 0
for x in range(N):
    for y in range(N):
        S += (x-C)**2 + (y-C)**2 + 1

# スコア計算
def calc_score(pts):
    su = 0
    for x,y in pts:
        su += (x-C)**2 + (y-C)**2 + 1    
    score = round(10**6 * N*N / M * su / S)
    return score

# 点追加
MOVE = ((-1,0),(0,-1),(1,0),(0,1))
DXY = ((1, 0),(1, 1),(0, 1),(-1, 1),(-1, 0),(-1, -1),(0, -1),(1, -1))
def add_point(pts,rects,used):

    # 制約を満たしつつその座標に点を追加できるかの判定
    def is_add_ok(x,y):

        # 既にその座標に点が存在する場合は不可
        if (x,y) in pts:
            return set([])

        # 2点目を探す際に、1点目との距離が短い点から探索
        cand_pts = []
        for x2,y2 in pts:
            dist = (x2-x)**2 + (y2-y)**2
            cand_pts.append((dist,x2,y2))
        cand_pts.sort()

        # 各点に対して、長方形の候補になりうるかを判定
        cand_rects = []
        for d,x2,y2 in cand_pts:
            dx,dy = x2-x, y2-y
            # y軸に平行な線分の場合
            if dx == 0:
                # (x2,y2)とx軸に平行な線分をなす点を探す
                for x3,y3 in pts:
                    if (x2,y2) != (x3,y3) and y2 == y3:
                        # 4点目が既に存在すれば追加
                        if (x3,y) in pts:
                            circum_len = abs(dy)*2 + abs(x3-x2)*2
                            rect = ((x,y),(x2,y2),(x3,y3),(x3,y))
                            cand_rects.append((circum_len,rect))
            # x軸に平行な線分の場合
            elif dy == 0:
                # (x2,y2)とy軸に平行な線分をなす点を探す
                for x3,y3 in pts:
                    if (x2,y2) != (x3,y3) and x2 == x3:
                        # 4点目が既に存在すれば追加
                        if (x,y3) in pts:
                            circum_len = abs(dx)*2 + abs(y3-y2)*2
                            rect = ((x,y),(x2,y2),(x3,y3),(x,y3))
                            cand_rects.append((circum_len,rect))
            # y=x上に存在する線分の場合
            elif dx == dy:
                # (x2,y2)とy=xに垂直な線分をなす点を探す
                for x3,y3 in pts:
                    dx2,dy2 = x3-x2, y3-y2
                    if (x2,y2) != (x3,y3) and dx2 == -dy2:
                        # 4点目が既に存在すれば追加
                        if (x+dx2,y+dy2) in pts:
                            circum_len = ((dx**2+dy**2)**0.5)*2 + ((dx2**2+dy2**2)**0.5)*2
                            rect = ((x,y),(x2,y2),(x3,y3),(x+dx2,y+dy2))
                            cand_rects.append((circum_len,rect))
            # y=-x上に存在する線分の場合
            elif dx == -dy:
                # (x2,y2)とy=-xに垂直な線分をなす点を探す
                for x3,y3 in pts:
                    dx2,dy2 = x3-x2, y3-y2
                    if (x2,y2) != (x3,y3) and dx2 == dy2:
                        # 4点目が既に存在すれば追加
                        if (x+dx2,y+dy2) in pts:
                            circum_len = ((dx**2+dy**2)**0.5)*2 + ((dx2**2+dy2**2)**0.5)*2
                            rect = ((x,y),(x2,y2),(x3,y3),(x+dx2,y+dy2))
                            cand_rects.append((circum_len,rect))
        
        # 長方形をなす4点が見つからなかった場合
        if len(cand_rects) == 0:
            return set([])
        else:
            return set(cand_rects)

    # 追加する点の候補探索は、近傍に点が多く存在する点から反時計回りの螺旋状に行う
    cand_pts = []
    for x,y in pts:
        adj_pts = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (x+dx,y+dy) in pts:
                    adj_pts += 1
        cand_pts.append((adj_pts,x,y))
    cand_pts.sort(reverse=True)

    # 既にチェックした点はスキップ
    seen = set()
    cand_rects_all = set()
    # for x,y in pts:
    for _,x,y in cand_pts:

        # TLE対策
        now = time.time()
        if now - start >= TIME_LIMIT:
            return

        dir = 0
        dist = 1
        while 0<=x<N and 0<=y<N and dist <= MAX_DIST:
            # 螺旋状に進む
            for _ in range(dist):
                x,y = x+MOVE[dir][0], y+MOVE[dir][1]
                if not (0<=x<N and 0<=y<N):
                    break
                if (x,y) in seen:
                    continue
                # 点を追加できるかの判定(だめならrect=[])
                cand_rects_all |= is_add_ok(x,y)
                seen.add((x,y))
            else:
                # 方向転換
                dir = (dir+1)%4
                # 2回方向転換するごとに進む距離が1伸びる
                if dir%2 == 0:
                    dist += 1
                continue
            break
        else:
            continue
        break

    # 長方形をなす4点を長方形の外周が短い順にソート
    cand_rects_all = list(cand_rects_all)
    cand_rects_all.sort()

    for circum_len,rect in cand_rects_all:
        # 長方形の外周上に他の点が存在しないかの判定
        flg = True
        for i in range(4):
            sx,sy = rect[i]
            tx,ty = rect[(i+1)%4]
            dx,dy = 1 if tx-sx > 0 else 0 if tx == sx else -1, 1 if ty-sy > 0 else 0 if ty == sy else -1
            dir = 0
            for j in range(8):
                if DXY[j] == (dx,dy):
                    dir = j
                    break

            # 長方形の外周上の点(頂点除く)を探索
            while (sx,sy) != (tx,ty):
                # 既存の点が存在する場合
                if (sx,sy) != rect[i] and (sx,sy) in pts:
                    flg = False
                    break
                # 既存の長方形と外周を共有する場合
                if used[sx][sy][dir]:
                    flg = False
                    break
                sx,sy = sx+dx,sy+dy
                # 既存の長方形と外周を共有する場合その2
                if used[sx][sy][dir^4]:
                    flg = False
                    break

            if not flg:
                break
    
        # 制約を満たす場合は長方形の4頂点を返す
        if flg:
            pts.add(rect[0])
            rects.append(rect)
            # 追加した長方形の外周に使用済みフラグを立てる
            for i in range(4):
                sx,sy = rect[i]
                tx,ty = rect[(i+1)%4]
                dx,dy = 1 if tx-sx > 0 else 0 if tx == sx else -1, 1 if ty-sy > 0 else 0 if ty == sy else -1
                dir = 0
                for j in range(8):
                    if DXY[j] == (dx,dy):
                        dir = j
                        break
                while (sx,sy) != (tx,ty):
                    used[sx][sy][dir] = True
                    sx,sy = sx+dx,sy+dy
                    used[sx][sy][dir^4] = True
            break

# メイン処理
max_score = calc_score(pts)
while 1:
    
    # TLE対策
    now = time.time()
    if now - start >= TIME_LIMIT:
        break

    # 状態のコピー作成
    # copy_pts = deepcopy(pts)
    # copy_ans = ans[:]
    # copy_used = deepcopy(used)

    # 点の追加
    add_point(pts,ans,used)
    # add_point(copy_pts,copy_ans,copy_used)

    # スコア計算
    score = calc_score(pts)

    # 上がってたら採用
    if score > max_score:
        max_score = score
        # pts = deepcopy(copy_pts)
        # ans = copy_ans[:]
        # used = deepcopy(copy_used)


# 結果出力
print(now-start,file=sys.stderr)
print(max_score,file=sys.stderr)
print(len(ans))
for a in ans:
    s = []
    for x,y in a:
        s.append(str(x))
        s.append(str(y))
    print(" ".join(s))