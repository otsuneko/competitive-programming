import time
import random
import math
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
SIMU_NUM = 500
TIME_LIMIT = 2
INF = 10**18

sy,sx,ty,tx,p =map(float,input().split())
sy,sx,ty,tx = int(sy),int(sx),int(ty),int(tx)
H =[list(input()) for _ in range(N)]
V =[list(input()) for _ in range(N-1)]
RANDOM_DIR = ["D"]*5 + ["R"]*5 + ["U"]*1 + ["L"]*1
RANDOM_DIR_LAST = ["D"]*1 + ["R"]*1 + ["U"]*(19-ty) + ["L"]*(19-tx)

path = bfs(sy,sx,ty,tx)
BFS_LENGTH = len(path)
# LIMIT_LENGTH = int(min(200, BFS_LENGTH*(3+p*5)))
LIMIT_LENGTH = 200

ans = path[:]
pre_path = []
max_score = simulation(sy,sx,ty,tx,p,ans)

start_temp = 500
end_temp = 1
START = time.time()
# オフィス到達確率を上げるためのシミュレーション
while 1:

    # TLE回避
    NOW = time.time()
    if NOW - START > 1.85:
        break

    # ランダムにdirを足していく。その際、高橋くんの忘却確率を重みとして付与。
    path = []
    for i,a in enumerate(ans):
        if len(path) < LIMIT_LENGTH:
            path.append(a)
        if len(path) == LIMIT_LENGTH:
            r_idx = random.randint(0,len(path)-1)
            r_prob = random.random()
            r_dir = random.choice(RANDOM_DIR_LAST)
            if r_prob < 0.1:
                path[r_idx] = r_dir
        else:
            r = random.random()
            if i < max(100,len(ans)*0.7):
                if r < 0.5:
                    r_dir = a
            else
                    r_dir = random.choice(RANDOM_DIR)
                else:
                    r_dir = random.choice(RANDOM_DIR_LAST)
                path.append(r_dir)
    # print("".join(path))

    # シミュレーション
    score = simulation(sy,sx,ty,tx,p,path)
    pre_score = simulation(sy,sx,ty,tx,p,pre_path)

    # temp = start_temp + (end_temp - start_temp) * (NOW-START) / TIME_LIMIT
    # prob = math.exp((score-pre_score)/temp)
    # print(prob)
    r = random.random()
    if score > max_score:
        if r < 0.95:
            max_score = score
            ans = path[:]
    
    pre_path = path[:]

print("".join(ans))