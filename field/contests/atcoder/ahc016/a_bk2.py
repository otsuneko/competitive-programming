import random
import sys
import time
from collections import defaultdict
from heapq import heappush, heappop
from collections import deque

# 定数
TIME_LIMIT = 5
NUM_QUERY = 100

# Hに一番近いグラフを事前生成したグラフから求める
def get_nearest_graph(H):
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
    # ERROR率>0の場合は、グラフの各頂点の出自数の合計で判定
    else:
        votes = [0]*M
        out_H = calc_outdegree(H)
        sum_H = sum(out_H)
        for s_k in range(M):
            for out in outdegrees[s_k]:
                diff = abs(sum_H - sum(out))
                if diff < 50:
                    votes[s_k] += 1
        # print("#votes_out:",votes_out)
        H_cnt_zero = H.count("0")
        for s_k, g in graphs_generated:
            diff = abs(H_cnt_zero - g.count("0"))
            # print("#diff:",diff)
            if diff < 50:
                votes[s_k] += 1
        # print("#votes:",votes)

        votes_hq = []
        for s_k,vote in enumerate(votes):
            heappush(votes_hq,(-vote,s_k))

        # 得票数が多い候補t_kのgraph CAND_NUM個に対し、outdegreeをソートした際に最も差分が大きくなる地点を基に正解予測
        max_diff = 0
        out_H.sort(reverse=True)
        print("#out_H_query:",out_H)
        CAND_NUM = 5
        for _ in range(CAND_NUM):
            if not votes_hq:
                break
            vote, s_k = heappop(votes_hq)
            if s_k+1 >= N:
                continue
            diff = out_H[s_k] - out_H[s_k+1]
            # print("#s_k,diff",s_k,diff)
            if diff >= max_diff:
                max_diff = diff
                t_k = s_k

    return t_k

# ランダムにHを生成する
def generate_H(graph):
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


##########################################メイン処理##########################################
# 入力
M,ERROR = map(str,input().split())
M = int(M)
ERROR = float(ERROR)

# 計測開始
start = time.time()

N = M
# ERROR=0の時はnC2 >= Mとなる最小のNを採用すれば100%正解可能
if ERROR == 0:
    for N in range(4,101):
        if N*(N-1)//2 >= M:
            break
elif ERROR < 0.05:
    GAP = 20
    for N in range(4,101):
        if N*(N-1)//2 >= GAP*M:
            break
    # N = min(100,M+1)
elif ERROR < 0.1:
    N = min(100,max(35,M+3))
elif ERROR < 0.15:
    N = min(100,max(40,M+3))
elif ERROR < 0.2:
    N = min(100,max(75,M+10))
else:
    N = 100

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
# ERROR<0.1の時は1と0の個数がGAPずつ増えていきつつ、頂点の出自数がピーキーになるようにグラフ生成
elif ERROR < 0.05:
    used_node_once = deque()
    used_node_twice = deque()
    print("#N,num_edges,GAP*M:",N,num_edges,GAP*M)
    graph = ["0"]*num_edges
    node_s = 0
    for i in range(M):
        # 全頂点から一度はGAP本の辺を張りに行った場合(2周目)
        if len(used_node_once) == N//2:
            node_s = used_node_once[0]
            used_node_twice.append(node_s)
            used_node_once.popleft()
            for j in range(1,GAP):
                node_t = node_s + GAP + j
                if node_s >= N or node_t >= N:
                    node_s, node_t = min(node_s%N, node_t%N),max(node_s%N, node_t%N)
                graph[graph_idx_map[(node_s,node_t)]] = "1"
            node_s = (node_s+GAP)%N
            graphs.append("".join(graph))
            print("#i,cnt_one,graph:",i,graph.count("1"),"".join(graph))
        # もしまだGAP本の辺を張りに行っていない頂点がある場合
        else:
            used_node_once.append(node_s)
            for j in range(1,GAP):
                node_t = node_s + j
                if node_s >= N or node_t >= N:
                    node_s, node_t = min(node_s%N, node_t%N),max(node_s%N, node_t%N)
                graph[graph_idx_map[(node_s,node_t)]] = "1"
            node_s = (node_s+GAP)%N
            graphs.append("".join(graph))
            print("#i,cnt_one,graph:",i,graph.count("1"),"".join(graph))

            while len(used_node_once) != N//2 and node_s in used_node_once:
                node_s = (node_s+1)%N
else:
    # ERROR率が0.2を越える場合は、グラフ毎に追加する辺に+50する
    NUM_ADD_EDGES = 50 if ERROR >= 0.2 else 1
    EDGE = N//2+NUM_ADD_EDGES
    graph = ["0"]*num_edges
    idx = 0
    for i in range(M):
        for j in range(1,EDGE):
        # for j in range(1,N//2+NUM_ADD_EDGES):
            # 偶数番目は頭から順に辺を張る
            if i%2 == 0:
                node_s = idx
                node_t = node_s + j
                if node_s >= N or node_t >= N:
                    node_s, node_t = min(node_s%N, node_t%N),max(node_s%N, node_t%N)
                graph[graph_idx_map[(node_s,node_t)]] = "1"
            # 奇数番目は真ん中から順に辺を張る
            else:
                node_s = N//2 + idx
                node_t = node_s + j
                if node_s >= N or node_t >= N:
                    node_s, node_t = min(node_s%N, node_t%N),max(node_s%N, node_t%N)
                graph[graph_idx_map[(node_s,node_t)]] = "1"
        if i%2:
            idx += 1
        graphs.append("".join(graph))


# グラフ毎にHを複数個乱数生成
graphs_generated = []
# グラフ毎にHを複数個乱数生成して各頂点の出自数を計算
outdegrees = defaultdict(list)
for s_k, graph in enumerate(graphs):
    outdegree = calc_outdegree(graph)
    print("#out:",sorted(outdegree,reverse=True))
    for i in range(10):
        H = generate_H(graph)
        # print("#H:",H)
        graphs_generated.append((s_k, H))
        outdegree = calc_outdegree(H)
        # print("#out_H:",sorted(outdegree,reverse=True))
        outdegrees[s_k].append(outdegree)


# グラフを出力
print(N,flush=True)
for g in graphs:
    print(g,flush=True)

# クエリ処理
for _ in range(NUM_QUERY):
    H = input()
    print(get_nearest_graph(H),flush=True)

    # now = time.time()
    # print("#time:",now-start,flush=True)