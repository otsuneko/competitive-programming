import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
graph = [[0]*N for _ in range(N)]
for a in range(N-1):
    D = list(map(int,input().split()))
    for i in range(len(D)):
        b = a+i+1
        graph[a][b] = graph[b][a] = D[i]

dp = [0]*(1<<N)

for bit in range(1<<N):
    s = -1
    for i in range(N):
        if bit>>i & 1 == 0:
            s = i
            break
    for to in range(N):
        if bit>>to & 1 == 0:
            nbit = bit | 1 << s | 1 << to
            dp[nbit] = max(dp[nbit], dp[bit] + graph[s][to])

print(max(dp))