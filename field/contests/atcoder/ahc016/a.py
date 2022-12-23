import random
import sys
import time
from collections import defaultdict
from copy import deepcopy

# 定数
TIME_LIMIT = 5
NUM_QUERY = 100

# Hに一番近いグラフを事前生成したグラフから求める
def get_nearest_graph(H, N, graphs_generated, degrees):
    t_k = M-1

    # ERROR率0の場合は、0の個数カウントすることで100%正解可能
    if ERROR == 0:
        min_diff = 10**18
        H_cnt_zero = H.count("0")
        # print("#H:",H)
        for s_k, g in graphs_generated:
            diff = abs(H_cnt_zero - g.count("0"))
            if diff < min_diff:
                min_diff = diff
                t_k = s_k
    # ERROR率>0の場合は、グラフの辺の数で正解候補を出した後グラフの各頂点の次数の落差が大きいインデックスで判定
    else:
        votes = [0]*M
        deg_H = calc_degree(H,N)
        sum_H = sum(deg_H)
        for s_k in range(M):
            for deg in degrees[s_k]:
                diff = abs(sum_H - sum(deg))
                # print("#diff_deg:",diff)
                if diff < 50:
                    votes[s_k] += 1
        
        H_cnt_zero = H.count("0")
        for s_k, g in graphs_generated:
            diff = abs(H_cnt_zero - g.count("0"))
            # print("#diff_zero:",diff)
            if diff < 50:
                votes[s_k] += 1
        # print("#votes:",votes)

        votes = sorted([ (x,i) for i, x in enumerate(votes)], reverse=True)
        
        # ERROR率が高くMも大きい場合は単純に辺の数で比較するのが良い
        if (ERROR == 0.39 and M >= 80) or ERROR == 0.40:
            s_k = votes[0][1]
            return s_k

        # 得票数が多い候補t_kのgraph CAND_NUM個に対し、degreeをソートした際に最も差分が大きくなる地点を基に正解予測
        max_diff = 1
        deg_H.sort(reverse=True)
        # print("#deg_H_query:",deg_H)
        CAND_NUM = 5
        for i in range(CAND_NUM):
            s_k = votes[i][1]
            for cand_t_k in range(max(0,s_k-1),min(M,s_k+2)):
                if cand_t_k+1 >= N:
                    # if max_diff < 2:
                    #     t_k = M-1
                    continue
                diff = deg_H[cand_t_k] - deg_H[cand_t_k+1]
                # print("#s_k,diff",s_k,diff)
                if diff > max_diff:
                    max_diff = diff
                    t_k = cand_t_k

    return t_k

# ランダムにHを生成する
def generate_H(graph, N):
    inv_graph = list(graph)
    # 辺を含むかを反転(=文字列の頭から確率ERRORで01反転)
    for i in range(num_edges):
        r = random.random()
        if r < ERROR:
            inv_graph[i] = "1" if inv_graph[i] == "0" else "0"
    # 頂点をシャッフル
    randomized_nodes = [i for i in range(N)]
    random.shuffle(randomized_nodes)
    H = [0]*num_edges
    for i in range(N):
        for j in range(i+1,N):
            ni,nj = min(randomized_nodes[i],randomized_nodes[j]), max(randomized_nodes[i],randomized_nodes[j])
            H[graph_idx_map[(ni,nj)]] = inv_graph[graph_idx_map[(i,j)]]
    return "".join(H)

# 各頂点の次数を計算
def calc_degree(graph, N):
    degree = [0]*N
    for i in range(N):
        for j in range(i+1,N):
            if graph[graph_idx_map[(i,j)]] == "1":
                degree[i] += 1
                degree[j] += 1
    return degree

##########################################メイン処理##########################################
# 入力
M,ERROR = map(str,input().split())
M = int(M)
ERROR = float(ERROR)

# 計測開始
start = time.time()

# Nをそのままと+1の2パターン試して良い方を採用
best_score = 0
best_N = 0
best_graphs = []
best_graphs_generated = []
best_degrees = []
for add_N in range(2):
    N = M
    # ERROR=0の時はnC2 >= Mとなる最小のNを採用すれば100%正解可能
    if ERROR == 0:
        for N in range(4,101):
            if N*(N-1)//2 >= M:
                break
    elif ERROR == 0.01:
        N_dic_001 = {10:14,11:12,12:12,13:14,14:14,15:16,16:16,17:18,18:18,19:20,20:20}
        if M in N_dic_001:
            N = N_dic_001[M]
        else:
            N = M+1 if M%2 else M
        N = min(100,N+add_N)
        GAP = N//2+1
    elif ERROR == 0.02:
        N_dic_002 = {10:16,11:14,12:14,13:14,14:16,15:18,16:18,17:20,18:20,19:20,20:20}
        if M in N_dic_002:
            N = N_dic_002[M]
        else:
            N = M+1 if M%2 else M
        N = min(100,N+add_N)
        GAP = N//2+1
    elif ERROR == 0.03:
        N_dic_003 = {10:18,11:16,12:16,13:16,14:16,15:20,16:20,17:20,18:20,19:20,20:20}
        if M in N_dic_003:
            N = N_dic_003[M]
        else:
            N = M+1 if M%2 else M
        N = min(100,N+add_N)
        GAP = N//2+1
    elif ERROR == 0.04:
        N_dic_004 = {10:22,11:20,12:20,13:20,14:20,15:22,16:22,17:22,18:24,19:24,20:24,21:22,22:24,23:26,24:26}
        if M in N_dic_004:
            N = N_dic_004[M]
        else:
            N = M+1 if M%2 else M
        N = min(100,N+add_N)
        GAP = N//2+1
    elif ERROR < 0.1:
        N = min(100,max(30,M+1))
        N = min(100,N+add_N)
        GAP = N//2+1
    elif ERROR < 0.15:
        N = min(100,max(40,M+3))
        N = min(100,N+add_N)
        GAP = N//2+1
    elif ERROR < 0.2:
        N = min(100,max(67,M+5))
        N = min(100,N+add_N)
        GAP = N//2+1
    elif ERROR < 0.25:
        GAP = 99 if M < 90 else 50
        for N in range(4,101):
            if N*(N-1)//2 >= GAP*M:
                break
        N = min(100,N+add_N)
    elif ERROR < 0.30:
        GAP = 99
        for N in range(4,101):
            if N*(N-1)//2 >= GAP*M*1.5:
                break
        N = min(100,N+add_N)
    elif ERROR < 0.35:
        GAP = 99
        for N in range(4,101):
            if N*(N-1)//2 >= GAP*M*2:
                break
        N = min(100,N+add_N)
    else:
        GAP = 99
        for N in range(4,101):
            if N*(N-1)//2 >= GAP*M*2.5:
                break
        N = min(100,N+add_N)

    # 全頂点間に辺を張った場合の辺の数
    num_edges = N*(N-1)//2

    # 辺の(始点,終点)のペアとグラフを01文字列変換した時のインデックスマップ
    graph_idx_map = dict()
    idx = 0
    for i in range(N):
        for j in range(i+1,N):
            graph_idx_map[(i,j)] = idx
            idx += 1

    graphs = []
    # ERROR=0の時は1と0の個数の比率が異なるグラフを生成するだけで100%正解可能
    if ERROR == 0:
        for k in range(0,num_edges,max(1,num_edges//M)):
            graphs.append("1"*k + "0"*(num_edges-k))
            graphs = graphs[:M]
    else:
        graph = ["0"]*num_edges
        idx = 0
        for i in range(M):
            for j in range(1,GAP):
                # 偶数番目は頭から順に辺を張る
                if i%2 == 0:
                    node_s = idx
                    node_t = (node_s + j)%N
                    if node_s == node_t:
                        continue
                    node_s, node_t = min(node_s%N, node_t%N),max(node_s%N, node_t%N)
                    graph[graph_idx_map[(node_s,node_t)]] = "1"
                # 奇数番目は真ん中から順に辺を張る
                else:
                    node_s = (N//2 + idx)%N
                    node_t = (node_s + j)%N
                    if node_s == node_t:
                        continue
                    node_s, node_t = min(node_s%N, node_t%N),max(node_s%N, node_t%N)
                    graph[graph_idx_map[(node_s,node_t)]] = "1"
            if i%2:
                idx = (idx+1)%N
            graphs.append("".join(graph))

    # グラフ毎にHを複数個乱数生成
    graphs_generated = []
    # グラフ毎にHを複数個乱数生成したものから各頂点の次数を計算
    degrees = defaultdict(list)
    for s_k, graph in enumerate(graphs):
        degree = calc_degree(graph,N)
        # print("#deg:",sorted(degree,reverse=True))
        for i in range(10):
            H = generate_H(graph,N)
            graphs_generated.append((s_k, H))
            degree = calc_degree(H,N)
            degrees[s_k].append(degree)

    # スコアをシミュレーション
    E = 0
    score = 0
    for _ in range(1):
        for _ in range(NUM_QUERY):
            s_k = random.randint(0,M-1)
            H = generate_H(graphs[s_k],N)
            t_k = get_nearest_graph(H,N,graphs_generated,degrees)
            if s_k != t_k:
                E += 1
        score += round(10**9 * (0.9**E) / N)
    print("#score,N",score,N)
    if score > best_score:
        best_score = score
        best_N = N
        best_graphs = deepcopy(graphs)
        best_graphs_generated = deepcopy(graphs_generated)
        best_degrees = deepcopy(degrees)
    
    if N+add_N >= 100:
        break
    # now = time.time()
    # if now-start >= 3:
    #     break


# 全頂点間に辺を張った場合の辺の数
num_edges = best_N*(best_N-1)//2
# 辺の(始点,終点)のペアとグラフを01文字列変換した時のインデックスマップ
graph_idx_map = dict()
idx = 0
for i in range(best_N):
    for j in range(i+1,best_N):
        graph_idx_map[(i,j)] = idx
        idx += 1

# グラフを出力
print(best_N,flush=True)
for g in best_graphs:
    print(g,flush=True)

# クエリ処理
for _ in range(NUM_QUERY):
    H = input()
    print(get_nearest_graph(H, best_N, best_graphs_generated, best_degrees),flush=True)

    now = time.time()
    print("#time:",now-start,flush=True)