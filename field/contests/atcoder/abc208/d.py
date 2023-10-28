#d[i][j]は2頂点間i, j間の移動コストを格納, Vは頂点数
INF = 10**18
def Warshall_Floyd(d,nxt,n):
    ans = 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]!=INF and d[k][j]!=INF:
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        nxt[i][j] = nxt[i][k]
                    elif k != i and d[i][k] + d[k][j] == d[i][j]:
                        nxt[i][j] = min(nxt[i][j], nxt[i][k]) #辞書順最小化
                if d[i][j] != INF:
                    ans += d[i][j]

    print(ans)

#s→tの最短経路復元
def get_path(s,t):
    if dist[s][t] == INF:
        return []
    path = [s]
    curr = s
    while curr != t:
        curr = nxt[curr][t]
        path.append(curr)
    return path

#隣接行列で経路を格納
N,M = map(int, input().split())
dist = [[INF]*N for _ in range(N)]
for i in range(M):
    s,t,d = map(int, input().split())
    s,t = s-1,t-1
    dist[s][t] = d

#s,tが同じ場合は距離0
for i in range(N):
    dist[i][i] = 0

#経路復元用
nxt = [[0]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        nxt[i][j] = j

Warshall_Floyd(dist,nxt,N)
