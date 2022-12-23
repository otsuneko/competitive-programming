N = int(input())
max_t = 0
tmp = []
for _ in range(N):
    # 時刻 Tに座標 Xの穴から出てきて、大きさは A
    t,x,a = map(int,input().split())
    max_t = max(max_t,t)
    tmp.append((t,x,a))

snuke = [[0]*5 for _ in range(max_t+1)]
for t,x,a in tmp:
    snuke[t][x] = a

dp = [[0]*5 for _ in range(max_t+1)]
isExist = [[False]*5 for _ in range(max_t+1)]
isExist[0][0] = True

for t in range(max_t):
    for x in range(5):
        if not isExist[t][x]:
            continue
        if x-1 >= 0:
            dp[t+1][x-1] = max(dp[t+1][x-1], dp[t][x] + snuke[t+1][x-1])
            isExist[t+1][x-1] = True
        if x+1 < 5:
            dp[t+1][x+1] = max(dp[t+1][x+1], dp[t][x] + snuke[t+1][x+1])
            isExist[t+1][x+1] = True        
        dp[t+1][x] = max(dp[t+1][x], dp[t][x] + snuke[t+1][x])
        isExist[t+1][x] = True

# print(*dp, sep="\n")

print(max(dp[max_t]))