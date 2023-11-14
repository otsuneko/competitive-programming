import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K,P = map(int,input().split())
idea = [list(map(int,input().split())) for _ in range(N)]

from collections import defaultdict

dp = [defaultdict(lambda: INF) for _ in range(N+1)]
dp[0][tuple([0]*K)] = 0

for i in range(N):
    dic = defaultdict(lambda:INF)
    for key,val in dp[i].items():
        tmp = [0]*K
        for j,p in enumerate(key):
            tmp[j] = min(P,p+idea[i][j+1])
        dic[tuple(tmp)] = min(dic[tuple(tmp)], val + idea[i][0])
        dic[key] = min(dic[key],val)

    for key,val in dic.items():
        dp[i+1][key] = val

# print(*dp, sep="\n")
if dp[N][tuple([P]*K)] == INF:
    print(-1)
else:
    print(dp[N][tuple([P]*K)])