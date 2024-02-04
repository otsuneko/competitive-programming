from typing import List
import sys
import time
import math
import random
from collections import deque
sys.setrecursionlimit(10**7)


# 定数
TIME_LIMIT = 2.0
INF = 10**18
MOVE = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIR = {"U":(-1,0), "R":(0,1), "D":(1,0), "L":(0,-1)}
INV_DIR = {(-1,0):"U", (0,1):"R", (1,0):"D", (0,-1):"L"}
VISIT_LIMIT = 5 # あるマスを訪れられる最大の回数

class Solver:

    def __init__(self, N: int, H: List[List[int]], V: List[List[int]], D: List[List[int]]):
        self.start = time.time()
        self.N = N
        self.H = H
        self.V = V
        self.D = D
        self.visited = set() # 訪れたことのあるマスの一覧
        self.visited.add((0,0))
        self.visit_count = [[0]*self.N for _ in range(self.N)] # 何回そのマスを訪れたか
        self.visit_count[0][0] = 1

    def solve(self) -> None:
        path = []
        # 全てのマスを踏破するまでループ
        cur_y,cur_x = 0,0
        while len(self.visited) != self.N**2:
            print(len(self.visited))
            print(*self.visit_count, sep="\n")
            now = time.time()
            if now - self.start >= TIME_LIMIT*0.8:
                break

            nxt_dir = self.bfs_decide_path(cur_y,cur_x)
            cur_y,cur_x = cur_y+DIR[nxt_dir][0], cur_x+DIR[nxt_dir][1]
            self.visited.add((cur_y,cur_x))
            self.visit_count[cur_y][cur_x] += 1
            path.append(nxt_dir)

        back_path = []
        if 0<=cur_y<self.N and 0<=cur_x<self.N:
            back_path = self.bfs_back_to_start(cur_y,cur_x)

        path += back_path

        # 全てのマスを踏破できていない、経路長が10**5を越える場合はサンプル解を提出する
        if len(self.visited) != self.N**2 or len(path) > 10**5:
            # self.emergency_solution()
            exit()

        print("".join(path))


    # BFSで次に進む方向を決める
    # まだ行ったことのないマスにたどり着ける最短ルートの方向&汚れが激しい方向
    def bfs_decide_path(self,sy,sx):
        cand_path_to_unvisited = []
        tmp_visit_count = [a[:] for a in self.visit_count]
        score,path = 0,[]
        queue = deque([[sy,sx,score,path]])
        while queue:
            y,x,score,path = queue.popleft()
            if self.visit_count[y][x] == 0:
                cand_path_to_unvisited.append((score/len(path),path))
                continue
            tmp_visit_count[y][x] += 1

            # 次に進んだほうがいい方向をスコア付け
            dir_score = {"U":-1, "R":-1, "D":-1, "L":-1}
            for dir in DIR:
                dy,dx = DIR[dir][0],DIR[dir][1]
                ny,nx = y+dy,x+dx
                if 0<=ny<self.N and 0<=nx<self.N and tmp_visit_count[ny][nx] < VISIT_LIMIT:
                    if dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0':
                        # 行った回数が少なく、汚れの激しいマスほどスコア大
                        dir_score[dir] = (self.D[ny][nx]) / (tmp_visit_count[ny][nx]+1)

            for dir in DIR:
                if dir_score[dir] == -1:
                    continue
                dy,dx = DIR[dir]
                ny,nx = y+dy,x+dx
                queue.append([ny, nx, score+dir_score[dir], path+[dir]])
        
        assert(len(cand_path_to_unvisited)>0)
        cand_path_to_unvisited.sort(reverse=True)
        path = cand_path_to_unvisited[0][1]
        nxt_dir = path[0]

        return nxt_dir

    # BFSで(0,0)まで戻る最短経路を求める
    def bfs_back_to_start(self,sy,sx):
        path = []
        queue = deque([[sy,sx,path]])
        visited = [[-1]*self.N for _ in range(self.N)]
        visited[sy][sx] = 0
        while queue:
            y,x,path = queue.popleft()
            if [y,x] == [0,0]:
                return path
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if 0<=ny<self.N and 0<=nx<self.N and visited[ny][nx] == -1:
                    if dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0':
                        visited[ny][nx] = visited[y][x] + 1
                        queue.append([ny, nx, path+[INV_DIR[(dy,dx)]]])


    # 答えが出なかった時はサンプルプログラムを出力
    def emergency_solution(self):
        visited = [[False for _ in range(self.N)] for _ in range(self.N)]
        DIJ = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        DIR = "RDLU"
        def dfs(i, j):
            visited[i][j] = True
            for dir in range(4):
                di, dj = DIJ[dir]
                i2 = i + di
                j2 = j + dj
                if 0 <= i2 < self.N and 0 <= j2 < self.N and not visited[i2][j2]:
                    if di == 0 and self.V[i][min(j, j2)] == '0' or dj == 0 and self.H[min(i, i2)][j] == '0':
                        print(DIR[dir], end='')
                        dfs(i2, j2)
                        print(DIR[(dir + 2) % 4], end='')
        dfs(0, 0)
        print()

def main():
    N = int(input())
    H = [list(input()) for _ in range(N-1)]
    V = [list(input()) for _ in range(N)]
    D = [list(map(int,input().split())) for _ in range(N)]
    solver = Solver(N, H, V, D)
    solver.solve()

if __name__ == "__main__":
    main()