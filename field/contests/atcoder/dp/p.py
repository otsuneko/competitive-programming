# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)
mod = 10**9+7

#0:白、1:黒
def dfs(s,pre):
    dp[s][0] = 1
    dp[s][1] = 1

    for to in graph[s]:
        if to != pre:
            dfs(to,s)
            dp[s][0] = dp[s][0] * (dp[to][0] + dp[to][1]) % mod
            dp[s][1] = dp[s][1] * dp[to][0] % mod

N = int(input())
graph = [[] for _ in range(N)]
for _ in range(N-1):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

dp = [[0]*2 for _ in range(N)]
dfs(0,-1)

print((dp[0][0]+dp[0][1])%mod)