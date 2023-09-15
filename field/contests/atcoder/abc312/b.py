import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]

ans = []
for i in range(N):
    for j in range(M):
        if not (0<=i+8<N and 0<=j+8<M):
            continue
        flg = True
        for k in range(9):
            for l in range(9):
                if k < 3 and l < 3:
                    if S[i+k][j+l] != "#":
                        flg = False
                elif k >= 6 and l >= 6:
                    if S[i+k][j+l] != "#":
                        flg = False
        if not (S[i+3][j] == S[i+3][j+1] == S[i+3][j+2] == S[i+3][j+3] == S[i][j+3] == S[i+1][j+3] == S[i+2][j+3] == "."):
            flg = False
        if not (S[i+5][j+5] == S[i+5][j+6] == S[i+5][j+7] == S[i+5][j+8] == S[i+6][j+5] == S[i+7][j+5] == S[i+8][j+5] == "."):
            flg = False
        if flg == True:
            ans.append((i+1,j+1))

if not ans:
    print()
else:
    for a in ans:
        print(*a)