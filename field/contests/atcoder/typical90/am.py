# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)

def dfs(s,pre):
    global ans
    dp[s] = 1

    for to in graph[s]:
        if to != pre: # to == preが葉(末端ノード)を表す
            dfs(to,s)
            dp[s] += dp[to]

    ans += dp[s] * (N-dp[s])

N = int(input())
graph = [[] for _ in range(N)]
for _ in range(N-1):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

dp = [0]*N
ans = 0
dfs(0,-1)
print(ans)