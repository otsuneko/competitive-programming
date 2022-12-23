def lcs_count(S, T):
    L1 = len(S)
    L2 = len(T)
    dp = [[0]*(L2+2) for i in range(L1+2)]
    sdp = [[0]*(L2+2) for i in range(L1+2)]
    dp[0][0] = 1
    sdp[1][1] = 1
 
    for i in range(L1+1):
        for j in range(L2+1):
            if i == 0 and j == 0:
                continue
            if i-1 >= 0 and j-1 >= 0 and S[i-1] == T[j-1]:
                dp[i][j] = sdp[i][j]
            sdp[i+1][j+1] = (sdp[i+1][j] + sdp[i][j+1] - sdp[i][j] + dp[i][j]) % (10**9+7)

    # sdp[L1+1][L2+1] が部分文字列の個数
    return sdp[L1+1][L2+1]

N,M = map(int,input().split())
S = list(map(int,input().split()))
T = list(map(int,input().split()))
print(lcs_count(S,T))