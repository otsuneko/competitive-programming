from typing import List
import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')
import time
import random
from collections import deque
from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
import itertools
import operator
from collections import defaultdict


# 定数
TIME_LIMIT = 2.0
INF = 10**18
MOVE = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIR = {"D":(1,0), "L":(0,-1), "U":(-1,0), "R":(0,1)}
INV_DIR = {(1,0):"D", (0,-1):"L", (-1,0):"U", (0,1):"R"}

CLUSTER_SIZE = {20:(5,5,5,5), 21:(5,5,5,6), 22:(5,5,6,6), 23:(5,6,6,6), 24:(6,6,6,6),
                25:(6,6,6,7), 26:(6,6,7,7), 27:(6,7,7,7), 28:(7,7,7,7), 29:(7,7,7,8),
                30:(7,7,8,8), 31:(7,8,8,8), 32:(8,8,8,8), 33:(8,8,8,9), 34:(8,8,9,9),
                35:(8,9,9,9), 36:(9,9,9,9), 37:(9,9,9,10), 38:(9,9,10,10), 39:(9,10,10,10), 40:(10,10,10,10)
                }
# CLUSTER_SIZE = {20:(5,5,5,5), 21:(5,5,5,6), 22:(5,5,6,6), 23:(5,6,6,6), 24:(6,6,6,6),
#                 25:(5,5,5,5,5), 26:(5,5,5,5,6), 27:(5,5,5,6,6), 28:(5,5,6,6,6), 29:(5,6,6,6,6),
#                 30:(5,5,5,5,5,5), 31:(5,5,5,5,5,6), 32:(5,5,5,5,6,6), 33:(5,5,5,6,6,6), 34:(5,5,6,6,6,6),
#                 35:(5,6,6,6,6,6), 36:(6,6,6,6,6,6), 37:(5,5,5,5,5,6,6), 38:(5,5,5,5,6,6,6), 39:(5,5,5,6,6,6,6), 40:(5,5,6,6,6,6,6)
#                 }

class Solver:

    def __init__(self, N: int, H: List[List[int]], V: List[List[int]], D: List[List[int]]):
        self.start = time.time()
        self.N = N
        self.H = H
        self.V = V
        self.D = D
        self.EDGE_NUM = 4

        self.cluster_id = [[-1]*(self.N) for _ in range(self.N)] # 各マスがどのクラスタに所属するか
        self.cluster_members = [set() for _ in range(self.EDGE_NUM**2)] # 各クラスタに所属するマスの集合
        self.neighbor_clusters = [set() for _ in range(self.EDGE_NUM**2)] # 各クラスタに隣接するクラスタ
        self.neighbor_cells = defaultdict(set) # 各クラスタの境界で隣接するマス
        self.ease_of_dirtiness = [0]*(self.EDGE_NUM**2) # 各クラスタの平均汚れやすさ
        self.visited_cells_in_cluster = [set() for _ in range(self.EDGE_NUM**2)] # 各クラスタ内の踏破済マス
        self.visited_cells = set() # 踏破済みマスの集合
        self.visited_cells_cnt = [[0]*self.N for _ in range(self.N)] # 各マスを何回通ったか
        self.clean_cluster_order = [] # 最終的なクラスタの掃除順序(全クラスタに到達するまで)
        self.clean_cell_order = [] # 最終的なマスの掃除順序

    def solve(self) -> None:
        # 盤面をBFSでいくつかの区画(クラスタ)に分割する
        # 各クラスタの平均汚れの差が最大になるように山登りor焼きなましで微調整する
        self._make_clusters()

        # クラスタ間の隣接関係をグラフ化して、最適な巡回順序を決定する
        # クラスタの窓口座標を決めて、そこからの巡回ルートも再帰的に決定する必要ありか
        self._decide_clean_route()
        print("".join(self.clean_cell_order))

    # 盤面をBFSでいくつかの区画に分割する
    def _make_clusters(self) -> None:
        # BFSで(0,0)から各マスへの距離を計算
        sy,sx = 0,0
        queue = deque([[sy,sx]])
        visited = [[-1]*self.N for _ in range(self.N)]
        visited[sy][sx] = 0
        while queue:
            y,x = queue.popleft()
            for dy,dx in MOVE:
                ny,nx = y+dy,x+dx
                if 0<=ny<self.N and 0<=nx<self.N and visited[ny][nx] == -1:
                    if dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0':
                        visited[ny][nx] = visited[y][x] + 1
                        queue.append([ny, nx])

        # print(*visited, sep="\n")
        
        # (0,0)からの距離に応じて各マスをCLUSTER_SIZE個のクラスタに分割
        cluster_size = CLUSTER_SIZE[self.N]
        cluster_size = list(itertools.accumulate(cluster_size, func=operator.add))
        for y in range(self.N):
            for x in range(self.N):
                cid = bisect(cluster_size,y)*self.EDGE_NUM + bisect(cluster_size,x)
                self.cluster_id[y][x] = cid
                self.cluster_members[cid].add((y,x))

        # 各クラスタ内のマスが全て隣接した状態になるようにクラスタ内のマスを再配置
        # BFSで到達不可能な同クラスタのマスは未割り当てに
        unassigned = set()
        for cid in range(self.EDGE_NUM**2):
            sy,sx = list(self.cluster_members[cid])[0]
            queue = deque([[sy,sx]])
            assigned = set()
            visited = [[-1]*self.N for _ in range(self.N)]
            visited[sy][sx] = 0
            while queue:
                y,x = queue.popleft()
                assigned.add((y,x))
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if 0<=ny<self.N and 0<=nx<self.N and visited[ny][nx] == -1 and (y,x) in self.cluster_members[cid]:
                        if dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0':
                            visited[ny][nx] = visited[y][x] + 1
                            queue.append([ny, nx])
            unassigned |= self.cluster_members[cid] - assigned

        # print(unassigned)

        # 未割り当てになったマスを隣接するマスが所属するクラスタに再割当て
        while len(unassigned) > 0:
            # print(*self.cluster_id, sep="\n", file=sys.stderr)
            # print(unassigned, file=sys.stderr)
            assigned = set()
            for y,x in unassigned:
                cand_cluster = set() # (隣接クラスタのメンバ数、隣接クラスタ)
                cid = self.cluster_id[y][x]
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx                    
                    if 0<=ny<self.N and 0<=nx<self.N and (ny,nx) not in unassigned:
                        ncid = self.cluster_id[ny][nx]
                        if (dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0'):
                            if cid != ncid:
                                cand_cluster.add((len(self.cluster_members[ncid]), ncid))
                            elif (y,x) in unassigned:
                                assigned.add((y,x))
                                break

                if len(assigned) > 0:
                    unassigned -= assigned
                    break

                if len(cand_cluster) == 0:
                    continue
                
                # (y,x)から辿れる全ての未割り当てマスを、一番メンバ数が少ないクラスタに割り当て
                cand_cluster = list(cand_cluster)
                cand_cluster.sort()
                _,ncid = cand_cluster[0]
                while 1:
                    cid = self.cluster_id[y][x]
                    self.cluster_members[cid].remove((y,x))
                    self.cluster_members[ncid].add((y,x))
                    self.cluster_id[y][x] = ncid
                    assigned.add((y,x))
                    for dy,dx in MOVE:
                        ny,nx = y+dy,x+dx
                        if 0<=ny<self.N and 0<=nx<self.N and (ny,nx) in unassigned and (ny,nx) not in assigned:
                            if (dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0'):
                                y,x = ny,nx
                                break
                    else:
                        break
                if len(assigned) > 0:
                    unassigned -= assigned
                    break
        
        print(*self.cluster_id, sep="\n", file=sys.stderr)
        # print(*self.cluster_members, sep="\n")

        # 各クラスタの隣接クラスタを格納
        # 各クラスタの平均汚れやすさも一緒に計算
        for y in range(self.N):
            for x in range(self.N):
                cid = self.cluster_id[y][x]
                for dy,dx in MOVE:
                    ny,nx = y+dy,x+dx
                    if 0<=ny<self.N and 0<=nx<self.N:
                        ncid = self.cluster_id[ny][nx]
                        if cid != ncid and (dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0'):
                            self.neighbor_clusters[cid].add(ncid)
                            self.neighbor_cells[(y,x)].add(((ny,nx),ncid))
                self.ease_of_dirtiness[cid] += self.D[y][x]
        
        for cid in range(self.EDGE_NUM**2):
            self.ease_of_dirtiness[cid] /= len(self.cluster_members[cid])
        
        # print(self.neighbor_clusters, file=sys.stderr)
        # print(self.neighbor_cells, file=sys.stderr)
        # print(self.ease_of_dirtiness, file=sys.stderr)


    # 最適なお掃除ルートを求める
    def _decide_clean_route(self):

        # まだ行ったことのないクラスタを優先的にお掃除
        # 汚れやすいクラスタは頻繁に、汚れにくいクラスタは時々お掃除
        # DFSでハミルトン路かそれに近いクラスタ巡回順序を求める
        path_list = []
        def _dfs_hamilton_path(cid,visited_clusters,path):
            # ハミルトン路に近く、汚れやすいクラスタを早く巡回するルートを高スコアとする
            score = 0
            for idx,cid in enumerate(path):
                score += self.ease_of_dirtiness[cid] * (len(path)-idx)
            score *= len(path)
            path_list.append((score, len(path), path))
            if len(path) == self.EDGE_NUM**2:                
                return

            for ncid in self.neighbor_clusters[cid]:
                if ncid not in visited_clusters:
                    visited_clusters.add(ncid)
                    _dfs_hamilton_path(ncid,visited_clusters,path+[ncid])
                    visited_clusters.remove(ncid)

        _dfs_hamilton_path(0,set([0]),[0])
        path_list.sort(reverse=True)
        # print(path_list, file=sys.stderr)

        # ハミルトン路ができていない場合に、未踏破のクラスタへ行く掃除順序を追加する
        def _dfs_unvisited_clusters(cid,visited_clusters,path):
            for ncid in self.neighbor_clusters[cid]:
                if ncid not in visited_clusters:
                    visited_clusters.add(ncid)
                    path = _dfs_unvisited_clusters(ncid,visited_clusters,path+[ncid])
            return path

        # TODO：最適な掃除順序を考える(疑似的な平均汚れが小さく、最後に訪れるクラスタが入口に近い程良いか)
        _, path_len, path = path_list[0]
        if path_len != self.EDGE_NUM**2:            
            best_path = []
            visited_clusters = set(path)
            for cid in path:
                best_path.append(cid)
                for ncid in self.neighbor_clusters[cid]:
                    if ncid not in visited_clusters:
                        visited_clusters.add(ncid)
                        path = _dfs_unvisited_clusters(ncid,visited_clusters,[ncid])
                        best_path += path
                        visited_clusters |= set(path)
        else:
            best_path = path_list[0][2]

        self.clean_cluster_order = best_path
        print(self.clean_cluster_order, file=sys.stderr)

        # 各クラスタ内のマスの掃除順序を決定する
        self.clean_cluster_order.append(-1)
        cur_y,cur_x = 0,0
        for i in range(len(self.clean_cluster_order)-1):
            cid,ncid = self.clean_cluster_order[i], self.clean_cluster_order[i+1]
            cur_y,cur_x = self._decide_clean_cell_order(cid,ncid,cur_y,cur_x)

        # 全クラスタ掃除できたら(0,0)に帰ってくるルートを求める
        # 単純にBFSで(0,0)までの最短距離を突き進む
        # TODO:帰りも汚れやすいセルを優先して帰る
        path = []
        queue = deque([[cur_y,cur_x,path]])
        visited = [[-1]*self.N for _ in range(self.N)]
        visited[cur_y][cur_x] = 0
        while queue:
            y,x,path = queue.popleft()
            if (y,x) == (0,0):
                self.clean_cell_order += path
                break
            for dir in DIR:
                dy,dx = DIR[dir]
                ny,nx = y+dy,x+dx
                if 0<=ny<self.N and 0<=nx<self.N and visited[ny][nx] == -1:
                    if dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0':
                        visited[ny][nx] = visited[y][x] + 1
                        queue.append([ny, nx, path+[dir]])


    # あるクラスタ内のマスを掃除する順序を決める
    def _decide_clean_cell_order(self,cid,ncid,cur_y,cur_x):

        # スタートマスからクラスタ内のマスを全て訪れる
        # ハミルトン路かそれに近い順序をDFSで探索(汚れやすいマス優先&次のクラスタに近いマスで終わってたらスコアアップ)
        # TODO:汚れがほぼないクラスタなら放置、汚れが多いクラスタなら踏破済みでももう一回掃除
        path_list = []
        def _dfs_hamilton_path(sy,sx,visited_cells,path):
            # ハミルトン路に近く、汚れやすいマスを早く巡回するルートを高スコアとする
            score = 0
            for idx,(y,x) in enumerate(path):
                score += self.D[y][x] * (len(path)-idx)
            score *= len(path)
            for dy,dx in MOVE:
                ny,nx = sy+dy,sx+dx
                # 最後のマスが次に巡回するクラスタに近ければスコアアップ
                if 0<=ny<self.N and 0<=nx<self.N and self.cluster_id[ny][nx] == ncid:
                    if dy == 0 and self.V[sy][min(sx, nx)] == '0' or dx == 0 and self.H[min(sy, ny)][sx] == '0':
                        score *= len(path)
                        break
            path_list.append((score, len(path), path))
            if len(path) == len(self.cluster_members[cid]):
                return
            
            for dir in DIR:
                dy,dx = DIR[dir]
                ny,nx = sy+dy,sx+dx
                if 0<=ny<self.N and 0<=nx<self.N and (ny,nx) not in visited_cells and cid == self.cluster_id[ny][nx]:
                    if dy == 0 and self.V[sy][min(sx, nx)] == '0' or dx == 0 and self.H[min(sy, ny)][sx] == '0':
                        # addとremoveで全パターン列挙するとTLEするため簡易版
                        visited_cells.add((ny,nx))
                        _dfs_hamilton_path(ny,nx,visited_cells,path+[(ny,nx)])
                        # visited_cells.remove((ny,nx))

        # ハミルトン路ができていない場合に、未踏破のマスへ行く掃除順序を追加する
        def _dfs_unvisited_cells(sy,sx,visited_cells,path):
            path_list2.append((len(path),path))
            for dir in DIR:
                dy,dx = DIR[dir]
                ny,nx = sy+dy,sx+dx
                if 0<=ny<self.N and 0<=nx<self.N and (ny,nx) not in visited_cells and cid == self.cluster_id[ny][nx]:
                    if dy == 0 and self.V[sy][min(sx, nx)] == '0' or dx == 0 and self.H[min(sy, ny)][sx] == '0':
                        visited_cells.add((ny,nx))
                        _dfs_unvisited_cells(ny,nx,visited_cells,path+[(ny,nx)])

        def _bfs(sy,sx,gy,gx,unvisited_cells):
            path = []
            queue = deque([[sy,sx,path]])
            visited = [[-1]*self.N for _ in range(self.N)]
            visited[sy][sx] = 0
            while queue:
                y,x,path = queue.popleft()
                if [y,x] == [gy,gx]:
                    for y,x in path:
                        if (y,x) in unvisited_cells:
                            unvisited_cells.remove((y,x))
                    return path
                for dir in DIR:
                    dy,dx = DIR[dir]
                    ny,nx = y+dy,x+dx
                    if 0<=ny<self.N and 0<=nx<self.N and visited[ny][nx] == -1 and cid == self.cluster_id[ny][nx]:
                        if dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0':
                            visited[ny][nx] = visited[y][x] + 1
                            queue.append([ny, nx, path+[(ny,nx)]])

        _dfs_hamilton_path(cur_y,cur_x,set([(cur_y,cur_x)]),[(cur_y,cur_x)])
        path_list.sort(reverse=True)
        # print(path_list[:3], file=sys.stderr)
        # ハミルトン路ができていない場合に、未踏破のマスへ行く掃除順序を追加する
        # TODO：最適な掃除順序を考える(疑似的な平均汚れが小さい掃除順序)
        _, path_len, path = path_list[0]
        # print(path)
        if path_len != len(self.cluster_members[cid]):
            best_path = []
            visited_cells = set(path)
            for y,x in path:
                best_path.append((y,x))
                for dir in DIR:
                    dy,dx = DIR[dir]
                    ny,nx = y+dy,x+dx
                    if 0<=ny<self.N and 0<=nx<self.N and (ny,nx) not in visited_cells and cid == self.cluster_id[ny][nx]:
                        if dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0':
                            visited_cells.add((ny,nx))
                            path_list2 = []
                            _dfs_unvisited_cells(ny,nx,visited_cells,[(ny,nx)])
                            path_list2.sort(reverse=True)
                            best_path += path_list2[0][1]
            
            # まだ未踏破のマスがある場合はBFSで踏破
            cur_y,cur_x = best_path[-1]
            unvisited_cells = self.cluster_members[cid] - visited_cells
            while len(unvisited_cells):
                gy,gx = list(unvisited_cells)[0]
                path = _bfs(cur_y,cur_x,gy,gx,unvisited_cells)
                best_path += path
                cur_y,cur_x = best_path[-1]
        else:
            best_path = path
        # print(best_path)
        cur_y,cur_x = best_path[-1]
        for i in range(len(best_path)-1):
            dy,dx = best_path[i+1][0]-best_path[i][0], best_path[i+1][1]-best_path[i][1]
            if (dy,dx) in MOVE:
                ndir = INV_DIR[(dy,dx)]
            else:
                unvisited_cells = set()
                path = _bfs(*best_path[i], *best_path[i+1], unvisited_cells)
                path = [best_path[i]] + path
                print(best_path)
                print(path)
                for i in range(len(path)-1):
                    dy,dx = path[i+1][0]-path[i][0], path[i+1][1]-path[i][1]
                    if (dy,dx) in MOVE:
                        ndir = INV_DIR[(dy,dx)]

            self.clean_cell_order.append(ndir)
        # print(self.clean_cluster_order, file=sys.stderr)
            
        # 最後のクラスタ(ncid==-1)なら次のクラスタ内のマスまで移動不要
        if ncid == -1:
            return cur_y,cur_x

        # 次に行くクラスタ内のマスまでBFSで移動する        
        path = []
        queue = deque([[cur_y,cur_x,path]])
        visited = [[-1]*self.N for _ in range(self.N)]
        visited[cur_y][cur_x] = 0
        while queue:
            y,x,path = queue.popleft()
            if self.cluster_id[y][x] == ncid:
                cur_y,cur_x = y,x
                self.clean_cell_order += path
                break
            for dir in DIR:
                dy,dx = DIR[dir]
                ny,nx = y+dy,x+dx
                if 0<=ny<self.N and 0<=nx<self.N and visited[ny][nx] == -1:
                    if dy == 0 and self.V[y][min(x, nx)] == '0' or dx == 0 and self.H[min(y, ny)][x] == '0':
                        visited[ny][nx] = visited[y][x] + 1
                        queue.append([ny, nx, path+[dir]])

        return cur_y,cur_x


def main():
    N = int(input())
    H = [list(input()) for _ in range(N-1)]
    V = [list(input()) for _ in range(N)]
    D = [list(map(int,input().split())) for _ in range(N)]
    solver = Solver(N, H, V, D)
    solver.solve()

if __name__ == "__main__":
    main()