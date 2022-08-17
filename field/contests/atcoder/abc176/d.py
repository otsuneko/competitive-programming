import sys
input = lambda: sys.stdin.readline().rstrip()
from collections import deque

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
def bfs(visited, sy, sx):
    global idx
    if section[sy][sx] != -1:
        return
    queue = deque([[sy, sx]])
    visited.add(sy*W+sx)

    while queue:
        y, x = queue.popleft()
        for dy, dx in move:
            new_y, new_x = y+dy, x+dx
            if 0 <= new_y < H and 0 <= new_x < W and maze[new_y][new_x] != "#" and new_y*W+new_x not in visited:
                    visited.add(new_y*W+new_x)
                    queue.append([new_y,new_x])

    for a in visited:
        x = a%W
        y = a//W
        section[y][x] = idx
    idx += 1
    return idx

from heapq import heappush, heappop
inf=10**18
def dijkstra(d,p,s):
    hq = [(0, s)] # (distance, node)
    seen = [False] * idx # ノードが確定済みかどうか
    while hq:
        v = heappop(hq)[1] # ノードを pop する
        seen[v] = True
        for to in dict[v]: # ノード v に隣接しているノードに対して
            if seen[to] == False and d[v] + 1 < d[to]:
                d[to] = d[v] + 1
                heappush(hq, (d[to], to))
                p[to] = v
    return dist

#s→tの最短経路復元
def get_path(t):
    if dist[t] == inf:
        return []
    path = []
    while t != -1:
        path.append(t)
        t = prev[t]
    #t->sの順になっているので逆順にする
    path.reverse()
    return path

H,W = map(int, input().split())
ch,cw = map(int,input().split())
dh,dw = map(int,input().split())
ch,cw,dh,dw = ch-1,cw-1,dh-1,dw-1
maze = [input() for _ in range(H)]
section = [[-1 for _ in range(W)] for _ in range(H)]

idx = 0
for y in range(H):
    for x in range(W):
        if maze[y][x] == "#":
            continue
        visited = set([])
        bfs(visited,y,x)

# print(*section, sep="\n")

move_warp = ([-2, -2], [-2, -1], [-2, 0], [-2, 1], [-2, 2], 
        [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], 
        [0, -2], [0, -1], [0, 1], [0, 2],
        [1, -2], [1, -1], [1, 0], [1, 1], [1, 2], 
        [2, -2], [2, -1], [2, 0], [2, 1], [2, 2])
start_idx = section[ch][cw]
goal_idx = section[dh][dw]
ans = 10**18
from collections import defaultdict
dict = defaultdict(set)
for y in range(H):
    for x in range(W):
        if maze[y][x] == "#":
            continue
        section_idx = section[y][x]
        for dy, dx in move_warp:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < W and 0 <= ny < H and section[ny][nx] != -1 and section[ny][nx] not in dict[section_idx]:
                dict[section_idx].add(section[ny][nx])

# print(dict)

dist = [inf]*idx
dist[start_idx] = 0
prev = [-1]*idx
dijkstra(dist,prev,start_idx)

if dist[goal_idx] == 10**18:
    print(-1)
else:
    print(dist[goal_idx])