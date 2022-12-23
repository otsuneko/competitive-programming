N =int(input())
T = input()

x,y = 0,0
dir = [1,0]
for t in T:
    if t == "S":
        x += dir[0]
        y += dir[1]
    else:
        if dir == [1,0]:
            dir = [0,-1]
        elif dir == [0,-1]:
            dir = [-1,0]
        elif dir == [-1,0]:
            dir = [0,1]
        else:
            dir = [1,0]

print(x,y)