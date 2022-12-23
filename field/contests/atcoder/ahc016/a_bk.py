import random
import sys
import time
from copy import deepcopy

# 定数
TIME_LIMIT = 5
NUM_QUERY = 100

# 計測開始
start = time.time()

# 入力
M,ERROR = map(str,input().split())
M = int(M)
ERROR = float(ERROR)

# Hに一番近いグラフを事前生成したグラフから求める
MOVE = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
def get_nearest_graph(H):
    t_k = 0

    # ERROR率0の場合は、0の個数カウントすることで100%正解可能
    if ERROR == 0:
        min_diff = 10**8
        H_cnt_zero = H.count("0")
        for s_k, g in enumerate(graphs):
            if abs(H_cnt_zero - g.count("0")) < min_diff:
                min_diff = abs(H_cnt_zero - g.count("0"))
                t_k = s_k
    # ERROR率>0の場合は、グラフの各頂点の出自数の合計で判定
    else:
        votes = [0]*M
        cand_t_k = 0
        out_H = calc_outdegree(H)
        sum_H = sum(out_H)
        for out,s_k in outdegrees:
            diff = abs(sum_H - out)
            if diff < 50:
                votes[s_k] += 1

        max_vote = 0
        for s_k,vote in enumerate(votes):
            if vote > max_vote:
                max_vote = vote
                cand_t_k = s_k
        t_k = cand_t_k

        # # 候補t_kの前後2個ずつの各graphに対し、matrix表現である(i,j)の周囲8マスを含めた辺の有無比較を実施
        # H2 = [["0"]*N for _ in range(N)]
        # idx = 0
        # for i in range(N):
        #     for j in range(i+1,N):
        #         H2[i][j] = H2[j][i] = H[idx]
        #         idx += 1
        
        # max_same = 0
        # for s_k in range(max(0,cand_t_k-2),min(M,cand_t_k)): # バグ取りのため範囲縮小中
        #     same = 0
        #     graph = [["0"]*N for _ in range(N)]
        #     idx = 0
        #     H3 = generate_H(graphs[s_k])
        #     for i in range(N):
        #         for j in range(i+1,N):
        #             graph[i][j] = graph[j][i] = H3[idx]
        #             idx += 1
        #     # print("#sk",s_k)
        #     # for i in range(N):
        #         # print("#",*graph[i])

        #     for i,j in graphs_pos_one[s_k]:
        #         same_one = 0
        #         for dy,dx in MOVE:
        #             ny,nx = i+dy,j+dx
        #             if not (0<=ny<N and 0<=nx<N):
        #                 continue
        #             # print("#i,j,H,graph:",ny,nx,H2[ny][nx] , graph[ny][nx])
        #             if H2[ny][nx] == graph[ny][nx] == "1":
        #                 same_one += 1
        #         if same_one >= 7:
        #             same += 1
        #     print("#s_k,same:",s_k,same)
        #     if same > max_same:
        #         max_same = same
        #         t_k = s_k

    return t_k

# ランダムにHを生成する
def generate_H(graph):
    H = list(graph)
    # 辺を含むかを反転(=文字列の頭から確率ERRORで01反転)
    for i in range(len(H)):
        r = random.random()
        if r < ERROR:
            H[i] = "1" if H[i] == "0" else "0"
    # 点をシャッフル(=文字列の順序をシャッフル)
    random.shuffle(H)
    H = "".join(H)
    return H    

# 各頂点の出自数を計算
def calc_outdegree(graph):
    outdegree = [0]*N
    idx = 0
    for i in range(N):
        for j in range(i+1,N):
            if graph[idx] == "1":
                outdegree[i] += 1
                outdegree[j] += 1
            idx += 1
    return outdegree

N = 4
# ERROR=0の時はnC2 >= Mとなる最小のNを採用
if ERROR == 0:
    for n in range(4,101):
        if n*(n-1)//2 >= M:
            N = n
            break
elif ERROR < 0.1:
    if M >= 70:
        N = M
    else:
        N = min(90,M+30)
else:
    N = min(100,M+45)
    
num_edges = N*(N-1)//2

# グラフの始点-終点のペアがHのどのインデックスに対応するかのマップ
graph_idx_map = dict()
idx = 0
for i in range(N):
    for j in range(i+1,N):
        graph_idx_map[(i,j)] = idx
        idx += 1

# 1と0の個数の比率を変えながらグラフ生成
graphs = []
graphs_pos_one = []
s_k = 0
for k in range(0,num_edges,max(1,num_edges//M)):
    graph = []
    graph_pos_one = set()
    cnt = 0
    for i in range(N):
        for j in range(i+1,N):
            if s_k%2:
                if cnt <= k:
                    graph.append("1")
                    graph_pos_one.add((i,j))
                    graph_pos_one.add((j,i))
                else:
                    graph.append("0")
            else:
                if cnt <= num_edges-k:
                    graph.append("0")
                else:
                    graph.append("1")
                    graph_pos_one.add((i,j))
                    graph_pos_one.add((j,i))
            cnt += 1
    graphs.append("".join(graph))
    graphs_pos_one.append(deepcopy(graph_pos_one))
    s_k += 1

graphs = graphs[:M]
graphs_pos_one = graphs_pos_one[:M]

# グラフ毎にHを複数個乱数生成し出自数の和を計算
outdegrees = []
for s_k, graph in enumerate(graphs):
    for i in range(50):
        H = generate_H(graph)
        outdegree = calc_outdegree(H)
        outdegrees.append((sum(outdegree),s_k))
    
# グラフを出力
print(N,flush=True)
for g in graphs:
    print(g,flush=True)

# クエリ処理
for _ in range(NUM_QUERY):
    H = input()
    print(get_nearest_graph(H),flush=True)

    now = time.time()
    print("#time:",now-start,flush=True)