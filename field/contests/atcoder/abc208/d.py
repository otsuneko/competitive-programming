#d[i][j]は2頂点間i, j間の移動コストを格納, Vは頂点数
inf = float("INF")
def warshall_floyd(d,nxt,n):
    global ans
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][k] + d[k][j], d[i][j])
                if d[i][j] != inf:
                    ans += d[i][j]

#s→tの最短経路復元
def get_path(s,t):
    if dist[s][t] == inf:
        return []
    path = [s]
    curr = s
    while curr != t:
        curr = nxt[curr][t]
        path.append(curr)
    return path

#隣接行列で経路を格納
N,M = map(int,input().split())
dist = [[inf]*N for _ in range(N)]
for i in range(M):
    A,B,C = map(int, input().split())
    A,B = A-1,B-1
    dist[A][B] = C
#s,tが同じ場合は距離0
for i in range(N):
    dist[i][i] = 0

#経路復元用
nxt = [[0]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        nxt[i][j] = j

ans = 0
warshall_floyd(dist,nxt,N)

print(ans)