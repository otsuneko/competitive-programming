N,M,K,S,T,X =map(int,input().split())
S,T,X = S-1,T-1,X-1
mod = 998244353

graph = [[] for _ in range(N)]
for _ in range(M):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

dp = [[[0]*2 for _ in range(N)] for _ in range(K+1)]
dp[0][S][0] = 1

for i in range(K):
    for v in range(N):
        for cntX in range(2):
            if dp[i][v][cntX] == 0:
                continue
            for to in graph[v]:
                if to == X:
                    dp[i+1][to][(cntX+1)%2] = (dp[i+1][to][(cntX+1)%2] + dp[i][v][cntX])%mod
                else:
                    dp[i+1][to][cntX] = (dp[i+1][to][cntX] + dp[i][v][cntX])%mod
# print(*dp, sep="\n")

print(dp[K][T][0])