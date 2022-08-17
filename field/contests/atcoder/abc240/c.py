N,X =map(int,input().split())
jumps =[list(map(int,input().split())) for _ in range(N)]

dp = [set() for _ in range(10001)]
dp[0].add(0)

for i in range(N):
    for j in jumps[i]:
        for x in range(10001):
            if i in dp[x]:
                dp[x+j].add(i+1)

print(["No","Yes"][N in dp[X]])