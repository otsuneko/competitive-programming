#d[i][j]は2頂点間i, j間の移動コストを格納, Vは頂点数
INF = 10**18
def Warshall_Floyd(d,n):
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]!=INF and d[k][j]!=INF:
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]

def is_ok(arg):
    #隣接行列で経路を格納
    dist = [[INF]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            manhattan = abs(jump[i][0]-jump[j][0]) + abs(jump[i][1]-jump[j][1])
            if jump[i][2]*arg >= manhattan:
                dist[i][j] = manhattan
            else:
                dist[i][j] = INF

    Warshall_Floyd(dist,N)

    for i in range(N):
        for j in range(N):
            if dist[i][j] == INF:
                break
        else:
            return True
    return False
    
def meguru_bisect(ng, ok):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok

N = int(input())
jump = [list(map(int,input().split())) for _ in range(N)]

ans = meguru_bisect(0,10**10)
print(ans)