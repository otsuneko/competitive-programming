from heapq import heappush, heappop
inf=10**18
dir = {"U":(-1,0), "R":(0,1), "D":(1,0), "L":(0,-1)}
def dijkstra(d,p,sy,sx):
    hq = [(0, (sy,sx))] # (distance, node)
    seen = [[False]*W for _ in range(H)] # ノードが確定済みかどうか
    while hq:
        y,x = heappop(hq)[1] # ノードを pop する
        seen[y][x] = True
        for key in dir:
            new_y, new_x = y+dir[key][0], x+dir[key][1]
            if not (0 <= new_y <= H-1 and 0 <= new_x <= W-1):
                continue

            cost = graph[new_y][new_x]
            if seen[new_y][new_x] == False and d[y][x] + cost < d[new_y][new_x]:
                d[new_y][new_x] = d[y][x] + cost
                heappush(hq, (d[new_y][new_x], (new_y, new_x)))
                p[new_y][new_x] = [y,x]

#最短経路復元
def get_path(ty,tx):
    path = []
    t = [ty,tx]
    while t != [-1,-1]:
        s = prev[t[0]][t[1]]
        d = (t[0]-s[0], t[1]-s[1])
        tmp = [k for k, v in dir.items() if v == d]
        if tmp:
            path.append(*tmp)
        t = s
    path.reverse()
    return path

#グラフのコスト更新
def update_graph_weight(cost,path,ty,tx):
    t = [ty,tx]
    graph[ty][tx] = cost//len(path)
    for p in path[::-1]:
        y = t[0] - dir[p][0]
        x = t[1] - dir[p][1]
        graph[y][x] = cost//len(path)
        t = [y,x]
        
H = W = 30
graph = [[1]*W for _ in range(H)]

for i in range(1000):

    # input position of start and goal
    sy,sx,ty,tx = map(int,input().split())
    sy,sx,ty,tx = sy-1, sx-1, ty-1, tx-1

    # calculate minimum path with dijkstra
    dist = [[inf]*W for _ in range(H)]
    dist[sy][sx] = 0
    prev =[[[-1,-1]]*W for _ in range(H)]
    dijkstra(dist,prev,sy,sx)
    path = "".join(get_path(ty,tx))
    print(path, flush=True)

    # update weights of the graph based on the given cost and the used path
    cost = int(input())
    update_graph_weight(cost,path,ty,tx)