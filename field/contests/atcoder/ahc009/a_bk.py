import time
import random
from collections import deque

DIR = ["D","R","U","L"]
MOVE = {"D":[1, 0], "R":[0, 1], "U":[-1, 0], "L":[0, -1]}
def bfs(sy, sx, ty, tx):
    path = []
    queue = deque([[sy,sx,path]])
    seen = [[-1]*N for _ in range(N)]
    seen[sy][sx] = 0
    while queue:
        y,x,path = queue.popleft()
        if [y,x] == [ty,tx]:
            return path
        for dir in DIR:
            ny,nx = y+MOVE[dir][0],x+MOVE[dir][1]
            if not (0<=ny<N and 0<=nx<N):
                continue
            if dir == "D" and (y < N-1 and V[y][x] == "1"):
                continue
            if dir == "U" and (y > 0 and V[y-1][x] == "1"):
                continue
            if dir == "R" and (x < N-1 and H[y][x] == "1"):
                continue
            if dir == "L" and (x > 0 and H[y][x-1] == "1"):
                continue
            if seen[ny][nx] == -1:
                seen[ny][nx] = seen[y][x] + 1
                path2 = path[:]
                path2.append(dir)
                queue.append([ny,nx,path2])

# SIMU_NUM回中何回高橋くんがオフィスにたどり着けるかをシミュレーション
def simulation(sy,sx,ty,tx,p,path):

    goal_cnt = 0
    for _ in range(SIMU_NUM):
        pos = [sy,sx]
        for step,dir in enumerate(path):
            if pos == [ty,tx]:
                # goal_cnt += 1/step
                goal_cnt += 1
                break
            r = random.random()
            # 進むべき方向を忘れるケース
            if r < p:
                continue
            # 忘れないケース
            else:
                pos = [pos[0]+MOVE[dir][0], pos[1]+MOVE[dir][1]]

    # 辿り着ける確率
    score = goal_cnt / SIMU_NUM
    return score

N = 20
SIMU_NUM = 100
RANDOM_DIR = ["D"]*5 + ["R"]*5 + ["U"]*2 + ["L"]*2

sy,sx,ty,tx,p =map(float,input().split())
sy,sx,ty,tx = int(sy),int(sx),int(ty),int(tx)
H =[list(input()) for _ in range(N)]
V =[list(input()) for _ in range(N-1)]

path = bfs(sy,sx,ty,tx)
BFS_LENGTH = len(path)
LIMIT_LENGTH = int(min(200, BFS_LENGTH*(10+p*10)))

ans = path[:]
max_score = simulation(sy,sx,ty,tx,p,ans)

START = time.time()
# オフィス到達確率を上げるためのシミュレーション
while 1:

    # TLE回避
    NOW = time.time()
    if NOW - START > 1.75 or len(ans) == LIMIT_LENGTH:
        break

    # ランダムにdirを足していく。その際、高橋くんの忘却確率を重みとして付与。
    path = []
    for a in ans:
        if len(path) >= LIMIT_LENGTH:
            break
        path.append(a)
        if len(path) >= LIMIT_LENGTH:
            break
        r = random.random()
        if r < p*4:
            r_dir = random.choice(RANDOM_DIR)
            path.append(r_dir)
    # print("".join(path))

    # シミュレーション
    score = simulation(sy,sx,ty,tx,p,path)
    if score > max_score:
        max_score = score
        ans = path[:]

print("".join(ans))