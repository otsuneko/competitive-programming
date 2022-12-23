from heapq import heappush, heappop
INF=10**18
def dijkstra(d,p,s):
    hq = [(0, s)] # (distance, node)
    while hq:
        cost,v = heappop(hq) # ノードを pop する
        if d[v] < cost:
            continue
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if d[v] + cost < d[to]:
                d[to] = d[v] + cost
                heappush(hq, (d[to], to))
                p[to] = v
    return d

#s→tの最短経路復元
def get_path(d,t):
    if d[t] == INF:
        return []
    path = []
    while t != -1:
        path.append(t)
        t = prev[t]
    #t->sの順になっているので逆順にする
    path.reverse()
    return path

# 入力の受け取り・隣接リストadjの構築：
N,M = map(int, input().split()) # ノード数, エッジ数
adj = [[] for _ in range(N)]
for _ in range(M):
    s,t,d = map(int, input().split())
    s,t = s-1,t-1
    adj[s].append((t, d))

dist1 = [INF]*N
dist1[0] = 0
prev = [-1]*N
dist1 = dijkstra(dist1,prev,0)
path = get_path(dist1,N-1) + [N-1]

memo = [INF]*N
for p in path:
    memo[p] = dist1[N-1]

for k in range(N):
    if dist1[k] == INF:
        print(-1)
    elif memo[k] < INF:
        print(memo[k])
    else:
        dist2 = [INF]*N
        dist2[k] = 0
        prev = [-1]*N
        dist2 = dijkstra(dist2,prev,k)
        path = get_path(dist2,N-1) + [N-1]
        for p in path:
            memo[p] = min(memo[p],dist1[k]+dist2[N-1])

        if memo[k] < INF:
            print(memo[k])
        else:
            print(-1)

'''
K - 旅行計画 / 
実行時間制限: 2 sec / メモリ制限: 1024 MB

配点 : 6 点

問題文
N 頂点 M 辺の重み付き有向グラフが与えられます。

頂点には 1 から N までの番号が振られています。
また、i (1≤i≤M) 本目の辺は頂点 u 
i
​
  から頂点 v 
i
​
  に向けて張られており、その重みは w 
i
​
  です。

k=1,2,…,N について、以下の問題を解いてください。

頂点 1 から始めて頂点 k を一度以上通り、頂点 N まで行く経路が存在するか判定し、存在するならそのうち最短のものの長さを出力せよ。
制約
2≤N≤2×10 
5
 
1≤M≤2×10 
5
 
1≤u 
i
​
 ,v 
i
​
 ≤N
u 
i
​
 

=v 
i
​
 
1≤w 
i
​
 ≤10 
9
 
入力はすべて整数
入力
入力は以下の形式で標準入力から与えられる。

N M
u 
1
​
  v 
1
​
  w 
1
​
 
u 
2
​
  v 
2
​
  w 
2
​
 
⋮
u 
M
​
  v 
M
​
  w 
M
​
 
出力
N 行にわたって出力せよ。i (1≤i≤N) 行目には k=i の場合の答えを以下に従って出力すること。

頂点 1 から始めて頂点 k を一度以上通り、頂点 N まで行く経路が存在するなら、そのうち最短のものの長さを出力。
頂点 1 から始めて頂点 k を一度以上通り、頂点 N まで行く経路が存在しないなら -1 を出力。
入力例 1 
Copy
3 3
1 2 3
2 3 4
1 3 2
出力例 1 
Copy
2
7
2
k=1 のとき、3 本目の辺を通って直接頂点 3 に移動する経路が最短です。
k=2 のとき、1 本目の辺を通って頂点 2 に移動したあと 2 本目の辺を通って頂点 3 に移動する経路が最短です。
k=3 のとき、3 本目の辺を通って直接頂点 3 に移動する経路が最短です。
入力例 2 
Copy
5 10
2 1 1
2 5 5
1 2 6
2 5 4
5 3 2
1 3 1
1 3 4
3 5 4
1 5 3
5 2 3
出力例 2 
Copy
3
10
5
-1
3
'''