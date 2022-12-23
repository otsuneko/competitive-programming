#d[i][j]は2頂点間i, j間の移動コストを格納, Vは頂点数
INF = 10**18
def Warshall_Floyd(d,n,K):
    global ans
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]!=INF and d[k][j]!=INF:
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
                    if k <= K:
                        ans += d[i][j]

#隣接行列で経路を格納
N,M = map(int, input().split())
roads = []
for i in range(M):
    s,t,d = map(int, input().split())
    s,t = s-1,t-1
    roads.append((s,t,d))

ans = 0
for K in range(N):
    dist = [[INF]*N for _ in range(N)]
    for s,t,d in roads:
        dist[s][t] = d

    #s,tが同じ場合は距離0
    for i in range(N):
        dist[i][i] = 0

    Warshall_Floyd(dist,K,N)

print(ans)