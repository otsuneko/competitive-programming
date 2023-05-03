N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]
T = [list(input()) for _ in range(M)]

ans = 0
for i in range(N):
    for j in range(M):
        if S[i][3:] == T[j]:
            ans += 1
            break

print(ans)