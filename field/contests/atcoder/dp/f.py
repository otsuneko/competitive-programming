def lcs(S, T):
    L1 = len(S)
    L2 = len(T)
    dp = [[0]*(L2+1) for i in range(L1+1)]
 
    for i in reversed(range(L1)):
        for j in reversed(range(L2)):
            if S[i] == T[j]:
                dp[i][j] = max(dp[i][j+1], dp[i+1][j], dp[i+1][j+1] + 1)
            else:
                dp[i][j] = max(dp[i][j+1], dp[i+1][j])

    # dp[0][0] が長さの解
    print(*dp, sep="\n")
    # ここからは復元処理
    res = []
    i = 0; j = 0
    while i < L1 and j < L2:
        if S[i] == T[j]:
            res.append(S[i])
            i += 1; j += 1
        elif dp[i][j] == dp[i+1][j]:
            i += 1
        elif dp[i][j] == dp[i][j+1]:
            j += 1
    return "".join(res)

S = input()
T = input()
print(lcs(S,T))