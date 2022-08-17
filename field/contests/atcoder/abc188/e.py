N,M = map(int,input().split())
A = list(map(int,input().split()))
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)

dp = [10**18]*N

for i in range(N):
    dp[i] = min(dp[i],A[i])
    for to in graph[i]:
        dp[to] = min(dp[to],dp[i],A[i])

ans = -10**18
for i in range(N):
    for to in graph[i]:
        ans = max(ans,A[to]-dp[i])

print(ans)