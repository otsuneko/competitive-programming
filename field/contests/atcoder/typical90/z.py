# submit as Python Code!!!! Not PyPy!!!!
import sys
sys.setrecursionlimit(10**7)
def dfs(pos,cur):
    global cnt_1
    global cnt_0
    color[pos] = cur
    if cur == 1:
        cnt_1 += 1
    elif cur == 0:
        cnt_0 += 1
    if cnt_1 >= N//2 or cnt_0 >= N//2:
        return

    for v in G[pos]:
        if color[v] == -1:
            dfs(v,1-cur)

N = int(input())
color = [-1]*N
cnt_1 = cnt_0 = 0
G = [[] for _ in range(N)]
for _ in range(N-1):
    s,t = map(int,input().split())
    s,t = s-1,t-1
    G[s].append(t)
    G[t].append(s)

dfs(0,0)
ans = []
cnt_1 = color.count(1)
cnt_0 = color.count(0)
for i in range(N):
    if len(ans) == N//2:
        break
    n = 1 if cnt_1 > cnt_0 else 0
    if color[i] == n:
        ans.append(i+1)

print(*ans)