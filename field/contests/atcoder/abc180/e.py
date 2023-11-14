import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

# https://atcoder.jp/contests/abc180/tasks/abc180_e
N = int(input())
cities = [list(map(int,input().split())) for _ in range(N)]

dp = [[INF]*N for _ in range(1<<N)]
# 都市1に着くためのコストは0
dp[1][0] = 0

#bitDP
for S in range(1<<N):
    for last in range(N):
        # lastに居ない場合はスキップ
        if S & (1 << last) == 0:
            continue
        for nxt in range(N):
            # 既にnxtに訪れている場合はスキップ
            if S & (1 << nxt):
                continue
            cx,cy,cz = cities[last]
            nx,ny,nz = cities[nxt]
            cost = abs(nx-cx) + abs(ny-cy) + max(0,nz-cz)
            dp[S|(1<<nxt)][nxt] = min(dp[S|(1<<nxt)][nxt], dp[S][last] + cost)

# 全ての都市を巡った後で都市1に戻ってくるコストの最小値
ans = INF
for last in range(N):
    cx,cy,cz = cities[last]
    nx,ny,nz = cities[0]
    cost = abs(nx-cx) + abs(ny-cy) + max(0,nz-cz)
    ans = min(ans, dp[(1<<N)-1][last] + cost)
print(ans)