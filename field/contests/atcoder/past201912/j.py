from heapq import heappush, heappop
INF=10**18

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
#move = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]) #縦横斜め移動
def dijkstra(y,x):
    hq = [(grid[y][x],y,x)]
    while hq:
        cost,y,x = heappop(hq)
        if dist[y][x] != cost:
            continue
        for dy,dx in move:
            ny,nx= y+dy,x+dx
            if not (0<=ny<H and 0<=nx<W):
                continue
            if dist[y][x] + grid[ny][nx] < dist[ny][nx]:
                dist[ny][nx] = dist[y][x] + grid[ny][nx]
                heappush(hq,(dist[ny][nx],ny,nx))
    return dist

H,W = map(int,input().split())
grid = [list(map(int,input().split())) for _ in range(H)]
dist = [[INF for _ in range(W)] for _ in range(H)]
dist[H-1][0] = grid[H-1][0]
D1 = dijkstra(H-1,0)
dist = [[INF for _ in range(W)] for _ in range(H)]
dist[H-1][W-1] = grid[H-1][W-1]
D2 = dijkstra(H-1,W-1)
dist = [[INF for _ in range(W)] for _ in range(H)]
dist[0][W-1] = grid[0][W-1]
D3 = dijkstra(0,W-1)

ans = INF
for y in range(H):
    for x in range(W):
        ans = min(ans,D1[y][x]+D2[y][x]+D3[y][x]-2*grid[y][x])

print(ans)
