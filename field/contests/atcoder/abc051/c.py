from collections import deque

move = {"U":[1, 0], "D":[-1, 0], "R":[0, 1], "L":[0, -1]}
dir = ["U","D","R","L"]
def bfs(sy,sx,gy,gx):
    queue = deque([[sy,sx]])
    while queue:
        y,x = queue.popleft()
        if [y,x] == [gy,gx]:
            return 
        for d in dir:
            ny,nx = y+move[d][0],x+move[d][1]
            if (ny,nx) not in seen:
                seen.add((ny,nx))
                dict[(ny,nx)] = dict[(y,x)][:]
                dict[(ny,nx)].append(d)
                queue.append([ny, nx])
            elif (ny,nx) == (gy,gx):
                dict[(ny,nx)] = dict[(y,x)][:]
                dict[(ny,nx)].append(d)
                return

from collections import defaultdict
sx,sy,tx,ty = map(int, input().split())

ans = []
seen = set([(sy,sx)])
dict = defaultdict(list)
bfs(sy,sx,ty,tx)
print(dict)