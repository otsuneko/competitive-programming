#d[i][j]は2頂点間i, j間の移動コストを格納, Vは頂点数
INF = 10**18
def Warshall_Floyd(d,nxt,n):
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]!=INF and d[k][j]!=INF:
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        nxt[i][j] = nxt[i][k]
                    elif k != i and d[i][k] + d[k][j] == d[i][j]:
                        nxt[i][j] = min(nxt[i][j], nxt[i][k]) #辞書順最小化

def calc_pair(X):

    #隣接行列で経路を格納
    dist = [[INF]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if A[i][j] == -1:
                dist[i][j] = X
            else:
                dist[i][j] = A[i][j]
        dist[i][i] = 0

    #経路復元用
    nxt = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            nxt[i][j] = j

    Warshall_Floyd(dist,nxt,N)

    #負経路の有無チェック
    for i in range(N):
        if dist[i][i] < 0:
            print("NEGATIVE CYCLE")
            exit()

    #全点対間距離の出力
    cnt = 0
    for i in range(N):
        for j in range(i+1,N):
            if dist[i][j] <= P:
                cnt += 1
    
    return cnt

def is_ok(arg,k):
    if calc_pair(arg) <= k:
        return True
    else:
        return False

def meguru_bisect(ng, ok,k):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid,k):
            ok = mid
        else:
            ng = mid
    return ok

# 入力の受け取り・隣接リストadjの構築：
N,P,K = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(N)]

if calc_pair(10**18) > K:
    print(0)
elif calc_pair(10**18) == K:
    print("Infinity")
else:
    ma = -1
    for i in range(N):
        for j in range(N):
            ma = max(ma,A[i][j])
    l = meguru_bisect(0,10**18,K)
    r = meguru_bisect(0,10**18,K-1)
    print(r-l)