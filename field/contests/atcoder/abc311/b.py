import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,D = map(int,input().split())
S = [list(input()) for _ in range(N)]

l = 0
ans = 0
for i in range(D):
    cnt = 0
    for j in range(N):
        if S[j][i] == "o":
            cnt += 1
    if cnt == N:
        l += 1
    else:
        ans = max(ans,l)
        l = 0
ans = max(ans,l)
print(ans)