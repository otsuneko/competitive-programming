import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W,K = map(int,input().split())
S = [list(input()) for _ in range(H)]
S_inv = inv = list(zip(*S))

ans = INF
if W >= K:
    for h in range(H):
        sw = S[h][:K]
        cnt_dot, cnt_maru = 0,0
        for c in sw:
            if c == ".":
                cnt_dot += 1
            elif c == "o":
                cnt_maru += 1
        if cnt_dot+cnt_maru == K:
            ans = min(ans,cnt_dot)
        for w in range(W-K-1):
            if S[h][w] == ".":
                cnt_dot -= 1
            elif S[h][w] == "o":
                cnt_maru -= 1
            
            if S[h][w+K] == ".":
                cnt_dot += 1
            elif S[h][w+K] == "o":
                cnt_maru += 1
            if cnt_dot+cnt_maru == K:
                ans = min(ans,cnt_dot)

if H >= K:
    for w in range(W):
        sw = S_inv[w][:K]
        cnt_dot, cnt_maru = 0,0
        for c in sw:
            if c == ".":
                cnt_dot += 1
            elif c == "o":
                cnt_maru += 1
        if cnt_dot+cnt_maru == K:
            ans = min(ans,cnt_dot)
        for h in range(H-K-1):
            if S_inv[w][h] == ".":
                cnt_dot -= 1
            elif S_inv[w][h] == "o":
                cnt_maru -= 1
            
            if S_inv[w][h+K] == ".":
                cnt_dot += 1
            elif S_inv[w][h+K] == "o":
                cnt_maru += 1
            if cnt_dot+cnt_maru == K:
                ans = min(ans,cnt_dot)

if ans == INF:
    print("-1")
else:
    print(ans)