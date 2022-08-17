# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)
import itertools

move = ([1, 0], [-1, 0], [0, 1], [0, -1])
def dfs2(y,x,seen):
    for dy, dx in move:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < N and 0 <= ny < N and seen[ny][nx] == False and ans[ny][nx] == '#':
            seen[ny][nx] = True
            dfs2(nx,ny,seen)

def judge():
    if cnt_vert.count(3) != N:
        return

    cnt = 0
    seen = [[False]*N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            seen[y][x] = True
            if ans[y][x] == "#" and seen[y][x] == False:
                cnt += 1
                dfs2(y,x,seen)
 
    print(cnt)
    if cnt == N:
        for a in ans:
            print("".join(a))
        exit()
    else:
        return False

def dfs(n):
    if n == N:
        # print(*ans, sep="\n")
        judge()
        return

    ptr = list(itertools.combinations(seq, 3))
    for p in ptr:
        for i in p:
            ans[n][i] = "#"
            cnt_vert[i] += 1
        if max(cnt_vert) <= 3:
            dfs(n+1)
        for i in p:
            ans[n][i] = "."
        for i in p:
            cnt_vert[i] -= 1

N = int(input())
seq = [i for i in range(N)]
ans = [["."]*N for _ in range(N)]
cnt_vert = [0]*N
dfs(0)