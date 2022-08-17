N,M = map(int, input().split())
edge = [0]*N
for i in range(M):
    x, y = map(int, input().split())
    edge[x-1] |= 1<<(y-1) # xがyより先にゴールした(グラフでxからyに遷移できる時のyをビットフラグで管理)

dp = [0]*(1<<N)
dp[0] = 1
for s in range(1, 1<<N):#集合を添字の小さい順に試す
    for i in range(N):#全ての要素を考える
        if ((s>>i)&1) and (not(edge[i]&s)):#i in sかつedge[i]とsが共通部分を持たない
            dp[s] += dp[s^(1<<i)]

# print(dp)
print(dp[(1<<N)-1])