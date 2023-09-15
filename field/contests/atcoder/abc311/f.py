import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]

for i in range(N):
    for j in range(M):
        if S[i][j] == "#":
            if i+1 < N:
                S[i+1][j] = "#"
                if j+1 < M:
                    S[i+1][j+1] = "#"

print(*S, sep="\n")