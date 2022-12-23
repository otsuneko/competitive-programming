N = int(input())
coins = list(map(int,input().split()))
coins.sort()

ans = float("INF")
money = 0
for i in range(10000):
    for j in range(10000):
        money = coins[2]*i+coins[1]*j
        if money > N:
            break
        elif (N-money)%coins[0] == 0:
            ans = min(ans,i+j+(N-money)//coins[0])
print(ans)