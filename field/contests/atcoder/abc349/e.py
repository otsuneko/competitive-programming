import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

def check_line(a):
    if a[0][0] == a[1][1] == a[2][2] == 'R':
        return "Takahashi"
    elif a[0][0] == a[1][1] == a[2][2] == 'B':
        return "Aoki"
    elif a[0][2] == a[1][1] == a[2][0] == 'R':
        return "Takahashi"
    elif a[0][2] == a[1][1] == a[2][0] == 'B':
        return "Aoki"

    for i in range(3):
        if a[i][0] == a[i][1] == a[i][2] == 'R':
            return "Takahashi"
        elif a[i][0] == a[i][1] == a[i][2] == 'B':
            return "Aoki"
        elif a[0][i] == a[1][i] == a[2][i] == 'R':
            return "Takahashi"
        elif a[0][i] == a[1][i] == a[2][i] == 'B':
            return "Aoki"
    return ""

def dfs(grid,turn):
    cnt = 0
    tak = ao = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] == "W":
                cnt += 1
            elif grid[i][j] == "R":
                tak += A[i][j]
            else:
                ao += A[i][j]
    if cnt == 9:
        if tak > ao:
            return True
        else:
            return False
    if check_line(grid) == "Takahashi":
        return True
    elif check_line(grid) == "Aoki":
        return False

    res = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == "W":
                if turn%2 == 0:
                    grid[i][j] = "R"
                    res.append(dfs(grid))
                    grid[i][j] = "W"
                else:
                    grid[i][j] = "B"
                    res.append(dfs(grid))
                    grid[i][j] = "W"
    print(res)
    return res

A = [list(map(int,input().split())) for _ in range(3)]
grid = [["W"]*3 for _ in range(3)]
dfs(grid,0)
