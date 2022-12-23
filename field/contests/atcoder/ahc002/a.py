import sys
sys.setrecursionlimit(10**7)
from collections import deque

def direction(dy,dx):
    if [dy,dx] == [1,0]:
        return "D"
    elif [dy,dx] == [-1,0]:
        return "U"
    elif [dy,dx] == [0,1]:
        return "R"
    elif [dy,dx] == [0,-1]:
        return "L"

def change_move_priority(y,x):
    t = [1 - y//25, 1 - x//25]

    # 現在地から見て右下が遠くに有る場合
    if t == [1,1]:
        if y < x:
            return ([1, 0], [0, 1], [0, -1], [-1, 0])
        else:
            return ([0, 1], [1, 0], [-1, 0], [0, -1])
    # 現在地から見て左下が遠くに有る場合
    elif t == [1,0]:
        if y < x-25:
            return ([1, 0], [0, -1], [0, 1], [-1, 0])
        else:
            return ([0, -1], [1, 0], [-1, 0], [0, 1])
    # 現在地から見て右上が遠くに有る場合
    elif t == [0,1]:
        if y-25 < x:
            return ([0, 1], [-1, 0], [1, 0], [0, -1])
        else:
            return ([-1, 0], [0, 1], [0, -1], [1, 0])
    # 現在地から見て左上が遠くに有る場合
    elif t == [0,0]:
        if y < x:
            return ([0, -1], [-1, 0], [1, 0], [0, 1])
        else:
            return ([-1, 0], [0, -1], [0, 1], [1, 0])

# def change_move_priority2(y,x):
#     print(y,x)
#     global move
#     if 0 <= y <= 10:
#         if 0 <= x <= 10:
#             move = ([1, 0], [0, 1], [0, -1], [-1, 0])
#         elif 40 <= x <= 49:
#             move = ([1, 0], [0, -1], [0, 1], [-1, 0])
#     elif 40 <= y <= 49:
#         if 0 <= x <= 10:
#             move = ([0, 1], [-1, 0], [1, 0], [0, -1])
#         elif 40 <= x <= 49:
#             move = ([0, -1], [-1, 0], [1, 0], [0, 1])

def dfs(y, x):
    global route
    global score
    global used_tile
    global move

    # change_move_priority2(y,x)
    for dy, dx in move:
        new_y, new_x = y+dy, x+dx
        if 0 <= new_y <= 49 and 0 <= new_x <= 49 and t[new_y][new_x] not in used_tile:
            used_tile.add(t[new_y][new_x])
            route[new_y][new_x] = route[y][x] + direction(dy,dx)
            score[new_y][new_x] = score[y][x] + p[y][x]
            dfs(new_y,new_x)

sy, sx = map(int, input().split())

t = [list(map(int,input().split())) for _ in range(50)]
p = [list(map(int,input().split())) for _ in range(50)]

route = [[""]*50 for i in range(50)]
score = [[0]*50 for i in range(50)]
used_tile = set([t[sy][sx]])

# move = change_move_priority(sy,sx)
move = ([1, 0], [-1, 0], [0, 1], [0, -1])
dfs(sy, sx)

best_score = 0
best_pos = [-1,-1]
best_route = ""
for y in range(50):
    for x in range(50):
        if score[y][x] > best_score:
            best_score = score[y][x]
            best_pos = [y,x]
            best_route = route[y][x]

# print(*route, sep="\n")
# print(*score, sep="\n")
print(best_score)
print(best_pos)
print(best_route)