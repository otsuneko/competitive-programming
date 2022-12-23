N,K = map(int,input().split())
N -= 1
MOD = 998244353
LR = [list(map(int,input().split())) for _ in range(K)]

dp = [0]*(N+1)
sdp = [0]*(N+2)
dp[0] = 1
sdp[1] = 1

for i in range(1,N+1):
    for l,r in LR:
        left = max(0,i-r)
        right = max(0,i-l+1)
        dp[i] += sdp[right]-sdp[left]
        dp[i] %= MOD
    sdp[i+1] = (sdp[i]+dp[i])%MOD
    # print(dp)
    # print(sdp)

print(dp[N])