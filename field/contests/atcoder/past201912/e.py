N,Q = map(int,input().split())
SNS = [[False]*N for _ in range(N)]
for _ in range(Q):
    S = list(map(int,input().split()))
    if S[0] == 1:
        a,b = S[1]-1,S[2]-1
        SNS[a][b] = True
    elif S[0] == 2:
        a = S[1]-1
        for i in range(N):
            if SNS[i][a] == True:
                SNS[a][i] = True
    elif S[0] == 3:
        a = S[1]-1
        tmp = set([])
        for i in range(N):
            # aがフォローしている人物i
            if SNS[a][i] == True:
                # aがフォローしているiがフォローしている人物j
                for j in range(N):
                    if j != a and SNS[i][j] == True:
                        tmp.add(j)
        for t in tmp:
            SNS[a][t] = True

for i in range(N):
    ans = ""
    for c in SNS[i]:
        ans += "Y" if c else "N"
    print(ans)

